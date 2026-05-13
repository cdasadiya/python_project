"""
Streamlit web app for the basic calculator.

Author: Chaitanya Dasadiya
GitHub: https://github.com/cdasadiya
"""

from dynamic_calculator import add, divide, multiply, subtract

OPERATIONS = {
    "Add": ("+", add),
    "Subtract": ("−", subtract),
    "Multiply": ("×", multiply),
    "Divide": ("÷", divide),
}


def calculate(operation: str, first_number: float, second_number: float) -> float:
    """Run the selected calculator operation."""
    _, operation_func = OPERATIONS[operation]
    return operation_func(first_number, second_number)


def main() -> None:
    """Render the Streamlit calculator application."""
    import streamlit as st

    st.set_page_config(page_title="Basic Calculator", page_icon="🧮")

    st.title("🧮 Basic Calculator")
    st.write("Enter two numbers, then click an operation button to calculate the result.")

    first_number = st.number_input("First number", value=0.0, step=1.0)
    second_number = st.number_input("Second number", value=0.0, step=1.0)

    st.subheader("Choose an operation")
    columns = st.columns(len(OPERATIONS))

    for column, (operation, (symbol, _)) in zip(columns, OPERATIONS.items()):
        if column.button(f"{symbol} {operation}", use_container_width=True):
            try:
                result = calculate(operation, first_number, second_number)
            except ZeroDivisionError as error:
                st.error(str(error))
            else:
                st.success(
                    f"{first_number:g} {symbol} {second_number:g} = {result:g}"
                )


if __name__ == "__main__":
    main()
