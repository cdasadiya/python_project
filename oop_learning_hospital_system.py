#!/usr/bin/env python3
"""
Hospital ERP OOP Learning Project (Single-File, Production-Style Demo)
======================================================================
This module is intentionally comprehensive: it implements a practical, menu-driven
Hospital Management mini-ERP while teaching core + advanced Python OOP concepts.

How to run:
- CLI app:      python oop_learning_hospital_system.py
- Test runner:  python oop_learning_hospital_system.py --run-tests
- OOP guide:    python oop_learning_hospital_system.py --oop-guide

Python version: 3.11+
Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import hashlib
import json
import logging
import os
import shutil
import tempfile
import threading
import time
import unittest
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Callable, Dict, Generator, Iterable, Iterator, List, Optional, Protocol, runtime_checkable


# ----------------------------- Logging Setup -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.FileHandler("hospital_app.log"), logging.StreamHandler()],
)
logger = logging.getLogger("hospital_app")


# ----------------------------- Exceptions -----------------------------
class AppError(Exception):
    """Base domain error used for controlled business failures."""


class ValidationError(AppError):
    """Raised when validation rules fail."""


class AuthenticationError(AppError):
    """Raised when login/auth checks fail."""


class AuthorizationError(AppError):
    """Raised when RBAC checks fail."""


class DataStoreError(AppError):
    """Raised for storage/serialization issues."""


# ----------------------------- Decorators -----------------------------
def audit(action: str) -> Callable:
    """Decorator for OOP action auditing; demonstrates decorators in OOP."""

    def decorate(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info("AUDIT action=%s method=%s", action, func.__qualname__)
            return func(*args, **kwargs)

        return wrapper

    return decorate


def requires_role(*allowed_roles: str) -> Callable:
    """RBAC decorator: authorization cross-cutting concern."""

    def decorate(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self: Any, actor: "User", *args: Any, **kwargs: Any) -> Any:
            if actor.role not in allowed_roles:
                raise AuthorizationError(f"Role '{actor.role}' cannot call {func.__name__}")
            return func(self, actor, *args, **kwargs)

        return wrapper

    return decorate


# ----------------------------- Interfaces-like Protocols -----------------------------
@runtime_checkable
class Notifier(Protocol):
    """Interface-like behavior via Protocol (duck-typed contract)."""

    def notify(self, message: str) -> None:
        ...


# ----------------------------- Validation -----------------------------
class Validator:
    """Static utility validator: shows static methods + reusable validation engine."""

    @staticmethod
    def non_empty(value: str, field_name: str) -> str:
        if not value or not value.strip():
            raise ValidationError(f"{field_name} must be non-empty")
        return value.strip()

    @staticmethod
    def positive_number(value: float, field_name: str) -> float:
        if value <= 0:
            raise ValidationError(f"{field_name} must be > 0")
        return value


# ----------------------------- Dataclasses + __slots__ -----------------------------
@dataclass(slots=True)
class MedicalRecord:
    """Value object with __slots__ optimization and explicit typing."""

    diagnosis: str
    medicines: List[str]
    notes: str


@dataclass(slots=True)
class Person:
    """Base entity for hierarchical inheritance."""

    id: str
    name: str
    age: int


@dataclass(slots=True)
class User(Person):
    """User for authentication/authorization and association with actions."""

    role: str
    _password_hash: str = field(repr=False, default="")

    @property
    def password_hash(self) -> str:
        """Read-only property to expose hidden value safely."""
        return self._password_hash

    @classmethod
    def create_with_password(cls, uid: str, name: str, age: int, role: str, password: str) -> "User":
        """Factory-like constructor class method."""
        return cls(id=uid, name=name, age=age, role=role, _password_hash=AuthService.hash_password(password))


@dataclass(slots=True)
class Patient(Person):
    """Patient extends Person; demonstrates overriding via methods downstream."""

    condition: str = "stable"


@dataclass(slots=True)
class Doctor(Person):
    """Doctor extends Person."""

    specialization: str = "General"


# ----------------------------- Inheritance Shapes -----------------------------
class TimestampMixin:
    """Mixin for multiple inheritance and MRO demo."""

    def stamp(self) -> str:
        return dt.datetime.now().isoformat(timespec="seconds")


class ContactMixin:
    """Second mixin for multiple inheritance."""

    def contact_signature(self) -> str:
        return "contact@hospital.local"


class Staff(Person, TimestampMixin):
    """Multilevel inheritance root for staff."""

    def __init__(self, id: str, name: str, age: int, staff_code: str):
        super().__init__(id=id, name=name, age=age)
        self.staff_code = staff_code


class Nurse(Staff):
    """Multilevel inheritance child class."""


class AdminStaff(Staff, ContactMixin):
    """Multiple inheritance: Staff + ContactMixin."""


class Billable(ABC):
    """Abstract base class to model interface-like contract."""

    @abstractmethod
    def calculate_bill(self) -> float:
        raise NotImplementedError


class Appointment(Billable):
    """Composition root: contains patient, doctor, and medical record."""

    service_fee: float = 250.0  # class variable

    def __init__(self, appointment_id: str, patient: Patient, doctor: Doctor, record: MedicalRecord):
        self.appointment_id = Validator.non_empty(appointment_id, "appointment_id")
        self.patient = patient  # association
        self.doctor = doctor    # aggregation/association
        self.record = record    # composition
        self._created_at = dt.datetime.now()

    def calculate_bill(self) -> float:
        return self.service_fee

    def summary(self) -> str:
        return f"{self.appointment_id}: {self.patient.name} -> Dr.{self.doctor.name}"

    def __repr__(self) -> str:
        return f"Appointment({self.appointment_id}, patient={self.patient.name})"

    def __lt__(self, other: "Appointment") -> bool:
        return self._created_at < other._created_at

    def __add__(self, other: "Appointment") -> float:
        return self.calculate_bill() + other.calculate_bill()


class EmergencyAppointment(Appointment):
    """Method overriding (calculate_bill), runtime polymorphism target."""

    def calculate_bill(self) -> float:
        return super().calculate_bill() * 1.5


# ----------------------------- Strategy Pattern -----------------------------
class BillingStrategy(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        raise NotImplementedError


class InsuranceStrategy(BillingStrategy):
    def apply(self, amount: float) -> float:
        return amount * 0.7


class NoDiscountStrategy(BillingStrategy):
    def apply(self, amount: float) -> float:
        return amount


# ----------------------------- Observer Pattern -----------------------------
class EventPublisher:
    def __init__(self):
        self._subscribers: List[Notifier] = []

    def subscribe(self, observer: Notifier) -> None:
        self._subscribers.append(observer)

    def publish(self, message: str) -> None:
        for sub in self._subscribers:
            sub.notify(message)


class LogNotifier:
    def notify(self, message: str) -> None:
        logger.info("NOTIFY: %s", message)


# ----------------------------- Singleton (thread-safe) -----------------------------
class ConfigManager:
    _instance: Optional["ConfigManager"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "ConfigManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.env = "prod"
        return cls._instance


# ----------------------------- File Handling + Context Manager -----------------------------
class JSONStore:
    """Persistence layer with context manager support and backup/restore."""

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self) -> "JSONStore":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write({"users": [], "patients": [], "doctors": [], "appointments": []})
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc:
            logger.exception("JSONStore exception: %s", exc)
        return False

    def read(self) -> Dict[str, Any]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception as e:
            raise DataStoreError(str(e)) from e

    def write(self, data: Dict[str, Any]) -> None:
        try:
            self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception as e:
            raise DataStoreError(str(e)) from e

    def backup(self, backup_path: Path) -> None:
        shutil.copy2(self.path, backup_path)

    def restore(self, backup_path: Path) -> None:
        shutil.copy2(backup_path, self.path)


# ----------------------------- Services -----------------------------
class AuthService:
    """Auth with encapsulation and method overloading simulation via *args."""

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def verify(self, user: User, password: str) -> bool:
        return user.password_hash == self.hash_password(password)

    def login(self, *args: Any) -> User:
        """Overloading simulation: login(user, pass) or login(id, pass, repo)."""
        if len(args) == 2 and isinstance(args[0], User):
            user, password = args
            if self.verify(user, password):
                return user
        elif len(args) == 3 and isinstance(args[0], str):
            user_id, password, repo = args
            user = repo.get_user(user_id)
            if user and self.verify(user, password):
                return user
        raise AuthenticationError("Invalid credentials")


class HospitalRepository(Iterable[Appointment]):
    """Repository implements iterable protocol and generator helpers."""

    def __init__(self, store: JSONStore):
        self.store = store
        self._appointments_cache: List[Appointment] = []

    def __iter__(self) -> Iterator[Appointment]:
        return iter(self._appointments_cache)

    def appointment_generator(self) -> Generator[Appointment, None, None]:
        for ap in self._appointments_cache:
            yield ap

    def load(self) -> None:
        raw = self.store.read()
        users = [User(**u) for u in raw["users"]]
        patients = {p["id"]: Patient(**p) for p in raw["patients"]}
        doctors = {d["id"]: Doctor(**d) for d in raw["doctors"]}
        appointments: List[Appointment] = []
        for a in raw["appointments"]:
            rec = MedicalRecord(**a["record"])
            cls = EmergencyAppointment if a.get("kind") == "emergency" else Appointment
            appointments.append(cls(a["appointment_id"], patients[a["patient_id"]], doctors[a["doctor_id"]], rec))
        self.users, self.patients, self.doctors = users, list(patients.values()), list(doctors.values())
        self._appointments_cache = appointments

    def save(self) -> None:
        data = {
            "users": [asdict(u) for u in self.users],
            "patients": [asdict(p) for p in self.patients],
            "doctors": [asdict(d) for d in self.doctors],
            "appointments": [
                {
                    "appointment_id": a.appointment_id,
                    "patient_id": a.patient.id,
                    "doctor_id": a.doctor.id,
                    "record": asdict(a.record),
                    "kind": "emergency" if isinstance(a, EmergencyAppointment) else "normal",
                }
                for a in self._appointments_cache
            ],
        }
        self.store.write(data)

    def get_user(self, uid: str) -> Optional[User]:
        return next((u for u in self.users if u.id == uid), None)


class HospitalService:
    """Business service (DIP): depends on abstractions/protocols, not concretes."""

    def __init__(self, repo: HospitalRepository, notifier: Notifier, strategy: BillingStrategy):
        self.repo = repo
        self.notifier = notifier
        self.strategy = strategy

    @audit("create_patient")
    @requires_role("admin", "staff")
    def add_patient(self, actor: User, patient: Patient) -> None:
        self.repo.patients.append(patient)
        self.repo.save()
        self.notifier.notify(f"Patient added: {patient.name}")

    @audit("create_appointment")
    @requires_role("admin", "staff", "doctor")
    def add_appointment(self, actor: User, ap: Appointment) -> float:
        self.repo._appointments_cache.append(ap)
        self.repo.save()
        amount = self.strategy.apply(ap.calculate_bill())
        self.notifier.notify(f"Appointment created {ap.appointment_id}, payable={amount}")
        return amount

    def report(self) -> Dict[str, Any]:
        total = sum(ap.calculate_bill() for ap in self.repo)
        return {
            "patients": len(self.repo.patients),
            "doctors": len(self.repo.doctors),
            "appointments": len(self.repo._appointments_cache),
            "gross_revenue": total,
        }


class EntityFactory:
    """Factory pattern for entity creation based on simple type keys."""

    @staticmethod
    def create_person(kind: str, **kwargs: Any) -> Person:
        mapping = {"patient": Patient, "doctor": Doctor, "user": User}
        if kind not in mapping:
            raise ValidationError(f"Unknown kind: {kind}")
        return mapping[kind](**kwargs)  # dynamic binding


class DynamicEntity:
    """Dynamic attribute handling and reflection demo class."""

    def __init__(self, **attrs: Any):
        for k, v in attrs.items():
            setattr(self, k, v)

    def __getattr__(self, item: str) -> Any:
        return f"<missing {item}>"


class AppointmentQueue:
    """Callable object + iterator-style queue wrapper."""

    def __init__(self, items: Optional[List[Appointment]] = None):
        self.items = items or []

    def __call__(self, ap: Appointment) -> None:
        self.items.append(ap)


class CLI:
    """Menu-driven CLI orchestrator."""

    def __init__(self, service: HospitalService, repo: HospitalRepository, auth: AuthService):
        self.service = service
        self.repo = repo
        self.auth = auth

    def run(self) -> None:
        print("\n--- Hospital ERP ---")
        print("1) Login & Dashboard  2) OOP Guide  3) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            self._login_flow()
        elif choice == "2":
            print(oop_concepts_guide())
        print("Bye!")

    def _login_flow(self) -> None:
        uid = input("User ID: ").strip()
        pw = input("Password: ").strip()
        user = self.auth.login(uid, pw, self.repo)
        rep = self.service.report()
        print(f"Welcome {user.name} ({user.role})")
        print("Dashboard:", rep)


def oop_concepts_guide() -> str:
    """Compact concept map covering requested OOP topics."""
    concepts = [
        "Classes/Objects, __init__, instance/class vars, instance/class/static methods",
        "Encapsulation, data hiding, properties, access modifiers convention",
        "Abstraction via ABC + Protocol interface-like contracts",
        "Inheritance types: single/multilevel/hierarchical/multiple + MRO + super()",
        "Polymorphism: overriding, dynamic binding, duck typing, strategy runtime selection",
        "Composition/aggregation/association in Appointment model",
        "Operator overloading (__add__, __lt__) and dunder methods (__repr__, __iter__, __call__, __getattr__)",
        "SOLID: SRP (services), OCP (strategies), LSP (Billable subtypes), ISP (Notifier protocol), DIP (DI)",
        "Patterns: Singleton, Factory, Strategy, Observer",
        "Exception handling, file handling, JSON serialization, logging, validation",
        "Type hints, dataclasses, __slots__, iterator/generator, reflection, metaprogramming basics (decorators)",
    ]
    return "\n".join(f"- {c}" for c in concepts)


def bootstrap_data(repo: HospitalRepository) -> None:
    if getattr(repo, "users", None):
        return
    admin = User.create_with_password("u1", "Alice", 34, "admin", "admin123")
    doctor_user = User.create_with_password("u2", "Bob", 41, "doctor", "doctor123")
    repo.users = [admin, doctor_user]
    repo.patients = [Patient("p1", "John", 28, "stable")]
    repo.doctors = [Doctor("d1", "Dr. Smith", 49, "Cardiology")]
    repo._appointments_cache = []
    repo.save()


# ----------------------------- Unit Tests -----------------------------
class HospitalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "db.json"
        with JSONStore(self.db_path) as store:
            self.repo = HospitalRepository(store)
            self.repo.load()
            bootstrap_data(self.repo)
        self.auth = AuthService()
        self.service = HospitalService(self.repo, LogNotifier(), InsuranceStrategy())

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_login(self) -> None:
        u = self.auth.login("u1", "admin123", self.repo)
        self.assertEqual(u.role, "admin")

    def test_create_appointment_and_bill(self) -> None:
        actor = self.auth.login("u1", "admin123", self.repo)
        rec = MedicalRecord("Flu", ["Med1"], "Rest")
        ap = EmergencyAppointment("a1", self.repo.patients[0], self.repo.doctors[0], rec)
        payable = self.service.add_appointment(actor, ap)
        self.assertGreater(payable, 0)

    def test_operator_overload(self) -> None:
        rec = MedicalRecord("A", [], "")
        a = Appointment("x1", self.repo.patients[0], self.repo.doctors[0], rec)
        b = EmergencyAppointment("x2", self.repo.patients[0], self.repo.doctors[0], rec)
        self.assertAlmostEqual(a + b, 625.0)


def run_tests() -> None:
    unittest.main(argv=["ignored"], exit=False, verbosity=2)


def demonstrate_advanced_features(repo: HospitalRepository) -> None:
    """Quick, safe runtime demos for reflection, duck typing, MRO, etc."""
    dyn = DynamicEntity(status="ok")
    setattr(dyn, "level", 5)
    _ = getattr(dyn, "status")
    _ = hasattr(dyn, "level")

    # duck typing with protocol-compatible notifier
    publisher = EventPublisher()
    publisher.subscribe(LogNotifier())
    publisher.publish("system started")

    # callable object
    q = AppointmentQueue(repo._appointments_cache)
    if repo.patients and repo.doctors:
        q(Appointment("callable-demo", repo.patients[0], repo.doctors[0], MedicalRecord("N/A", [], "")))

    # MRO demo
    _mro = AdminStaff.__mro__
    logger.info("MRO(AdminStaff): %s", _mro)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hospital ERP OOP Learning Project")
    parser.add_argument("--run-tests", action="store_true", help="Run built-in tests")
    parser.add_argument("--oop-guide", action="store_true", help="Print OOP concept guide")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.run_tests:
        run_tests()
        return
    if args.oop_guide:
        print(oop_concepts_guide())
        return

    db = Path("hospital_data.json")
    with JSONStore(db) as store:
        repo = HospitalRepository(store)
        repo.load()
        bootstrap_data(repo)
        demonstrate_advanced_features(repo)
        service = HospitalService(repo, LogNotifier(), NoDiscountStrategy())
        cli = CLI(service, repo, AuthService())
        try:
            cli.run()
        except AppError as e:
            logger.error("Application error: %s", e)


if __name__ == "__main__":
    main()
