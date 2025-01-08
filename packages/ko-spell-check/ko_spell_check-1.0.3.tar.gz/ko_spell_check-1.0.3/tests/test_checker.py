from kospellcheck import SpellChecker

checker = SpellChecker()

# Simple spelling check
result = checker.check_spelling("분의기!! @맞춤법$ 검사")
print(result)

# Clean text and check spelling
cleaned_result = checker.clean_text_and_check("분의기!! @맞춤법$ 검사")
print(cleaned_result)