import os
import requests
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_restaurants(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the restaurant listing of a website (TripAdvisor).
            Your job is to extract the restaurant details and return them in JSON format containing the following keys: 
            `restaurant_name`, `cuisine`, `rating`, `location`, `description`, `image_url`.
            Only return valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse restaurants.")
        return res if isinstance(res, list) else [res]

    def save_to_csv(self, restaurant_data, file_name="restaurants.csv"):
        df = pd.DataFrame(restaurant_data)
        df.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")

    def save_images(self, restaurant_data, image_folder="restaurant_images"):
        # Create the directory if it does not exist
        os.makedirs(image_folder, exist_ok=True)

        for restaurant in restaurant_data:
            if 'image_url' in restaurant and restaurant['image_url']:
                # Get the image URL
                image_url = restaurant['image_url']
                try:
                    # Send a GET request to download the image
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        # Create a file name based on the restaurant name
                        image_name = f"{restaurant['restaurant_name'].replace(' ', '_')}.jpg"
                        image_path = os.path.join(image_folder, image_name)

                        # Save the image
                        with open(image_path, 'wb') as f:
                            f.write(img_response.content)
                            print(f"Saved image for {restaurant['restaurant_name']} at {image_path}")
                    else:
                        print(
                            f"Failed to download image for {restaurant['restaurant_name']}. Status code: {img_response.status_code}")
                except Exception as e:
                    print(f"Error downloading image for {restaurant['restaurant_name']}: {e}")


if __name__ == "__main__":
    # Scraping the TripAdvisor page
    url = "https://www.swiggy.com/city/madurai/best-restaurants"

    # Set the headers with a valid User-Agent to simulate a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Make the request with headers
    response = requests.get(url, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print("Successfully retrieved the page.")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming you want to extract all visible text from the page
        cleaned_text = soup.get_text(separator=" ", strip=True)

        # Initialize Chain and extract restaurant details
        chain = Chain()
        restaurant_data = chain.extract_restaurants(cleaned_text)

        # Save the extracted data to CSV
        chain.save_to_csv(restaurant_data)

        # Save images of the restaurants
        chain.save_images(restaurant_data)

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
