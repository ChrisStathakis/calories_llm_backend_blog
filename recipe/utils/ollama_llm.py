import ollama
from deep_translator import GoogleTranslator

class OllamaService:

    def __init__(self, model="llama3.2:1b"):
        self.model = model

    def ask_llm(self, food: str):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": """Please provide the nutritional information per 100 grams for {0}. 
                    Return the response in the following JSON format:
                    {{
                        "food": "{0}",
                        "calories": 0,
                        "protein": 0,
                        "fats": 0,
                        "carbs": 0
                    }}
                    Ensure the values are numerical and represent the amount per 100 grams. and its json format and only this""".format(food)
                }
            ]
        )

        content = response['message']['content']
        return content

    def get_nutrition_info(self, sentence: str):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": """Extract foods and their amounts from this sentence: {0}
                    Return ONLY a list in this exact format with no other text:
                    [[food1, amount_in_grams], [food2, amount_in_grams], ...]
                    Rules:
                    - Amounts must be numbers, not strings
                    - Each food must be unique
                    - Return ONLY the list, no explanations or other text
                    - Amounts should be in grams
                    - Return 5 in amount_of_grams for the specific food if the sentence contains the word spoon or spoonful.
                    """.format(sentence)
                }
            ]
        )

        return response['message']['content']

    @staticmethod
    def translate_to_english(sentence: str):
        return GoogleTranslator(source='auto', target='english').translate(sentence)

    @staticmethod
    def string_to_list(input_str: str):
        # Your input string

        # Remove the outer brackets
        cleaned_str = input_str.strip("[]")

        # Split by "], [" to get each sublist
        sublist_strings = cleaned_str.split("], [")

        # Process each sublist
        result = []
        for sublist_str in sublist_strings:
            # Clean up any leftover brackets
            sublist_str = sublist_str.strip("[]")

            # Split by comma
            elements = sublist_str.split(",")

            # Process each element in the sublist
            sublist = []
            for element in elements:
                clean_element = element.strip()
                # Try to convert to int if it's a number
                try:
                    clean_element = int(clean_element)
                except ValueError:
                    # If not a number, remove any quotes if present
                    clean_element = clean_element.strip("'\"")

                sublist.append(clean_element)

            result.append(sublist)

        return result