import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simplex import Simplex

from PIL import ImageDraw

from playwright.sync_api import sync_playwright
from PIL import Image
import time
import tempfile
import webbrowser

from dotenv import load_dotenv

import io


load_dotenv()


def screenshot_tests():
    simplex = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"))
    image = "/home/ubuntu/supreme-waffle/images/netflix.png"
    screenshot = Image.open(image)

    start_time = time.time()
    bbox = simplex.find_element("dark mode icon", screenshot)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    print(bbox)

    start_time = time.time()
    action = simplex.step_to_action("click and enter email address", screenshot)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    print(action)


def execute_action_test():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    driver = browser.new_page()
    
    simplex = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"), driver=driver)
    simplex.goto("https://www.netflix.com/")
    actions = [['CLICK', 'email field'], ['TYPE', 'email address']]
    simplex.execute_action(actions[0])


def cgtrader_test():
    assets = ["apple watch"]
    urls = []

    with sync_playwright() as p:
        driver = p.chromium.launch(headless=False).new_page()
        simplex = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"), driver=driver)
        simplex.goto("https://www.cgtrader.com/")

        for asset in assets:
            simplex.goto("https://www.cgtrader.com")
            simplex.do(f"search for {asset}")  
            simplex.do("click on search button")
            simplex.do(f"click on the first product")
            driver.wait_for_timeout(3000)

            urls.append(simplex.driver.url)

    print(urls)


def test_find_element(): 
    simplex = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"))
    simplex.goto("https://www.cgtrader.com/")

    state = simplex.take_stable_screenshot()
    bbox = simplex.find_element("cart")
    
    # Save the screenshot without annotation
    state.save('screenshot_with_bbox.png')

    # Create a minimal HTML file with just the visualization and bbox
    with open('screenshot_with_bbox.html', 'w') as f:
        f.write(f"""
        <div style="position: relative; display: inline-block;">
            <img src="screenshot_with_bbox.png">
            <div style="
                position: absolute;
                border: 2px solid red;
                left: {bbox[0]}px;
                top: {bbox[1]}px;
                width: {bbox[2] - bbox[0]}px;
                height: {bbox[3] - bbox[1]}px;
                pointer-events: none;
            "></div>
        </div>
        """)

    # Create a second HTML file with just the screenshot
    with open('screenshot.html', 'w') as f:
        f.write("""
        <div style="position: relative; display: inline-block;">
            <img src="screenshot_with_bbox.png">
        </div>
        """)


if __name__ == "__main__":
    cgtrader_test()
    
    
