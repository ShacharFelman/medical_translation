import os
import sys
# from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.translation_service import TranslationService

def run_translation_test():
    # load_dotenv()  # Load environment variables from .env file

    # Initialize TranslationService
    translation_service = TranslationService()
    translation_service.initialize()

    # Hard-coded test parameters
    input_text = "נטילת מקיניסט או שילוב של מקיניסט עם דבראפניב יכולה לגרום לדימום חמור כולל במוח, במערכת העיכול (כגון בבטן, בפי הטבעת או במעי), בריאות ובאיברים אחרים, ועלולה להוביל למוות. התסמינים יכולים לכלול:"
    human_verified_translation = "Taking Mekinist or the combination of Mekinist and dabrafenib can cause serious bleeding including in the brain, the digestive system (such as stomach, rectum or intestine), lungs, and other organs, and can lead to death. Symptoms may include:"

    # Perform translation
    result = translation_service.translate(input_text, human_verified_translation)

    print(f"Translation result: {result}")
    print("Translation data has been saved to the database.")
    print("You can now check the results in MongoDB.")

if __name__ == "__main__":
    run_translation_test()