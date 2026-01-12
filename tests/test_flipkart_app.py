from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup Options ---
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Pixel 9 API 36.0"
options.udid = "emulator-5554"
options.app_package = "com.flipkart.android"
options.app_activity = "com.flipkart.android.activity.HomeFragmentHolderActivity"
options.no_reset = True
options.new_command_timeout = 300 

print("Initializing Driver...")
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
print("Flipkart app launched successfully")
time.sleep(6) 

# --- Task 1: Click Search Bar ---
print("Attempting to click Search Bar...")
try:
    search_bar = driver.find_element(
        AppiumBy.XPATH, 
        '//android.view.ViewGroup[@bounds="[162,405][798,531]"]'
    )
    search_bar.click()
    print("Search Bar clicked")
    time.sleep(3) 
except Exception as e:
    print(f"Error finding search bar: {e}")
    driver.quit()
    exit()

# --- Task 2: Type Query and Search ---
print("Typing 'boat earpods'...")
try:
    # Finding the EditText explicitly (More stable than active_element)
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
    )
    search_input.click()
    search_input.send_keys("boat earpods")
    print("Typed text successfully")
    
    driver.press_keycode(66) # Enter
    print("Pressed Enter key")
    
    # Hide keyboard just in case
    try:
        driver.hide_keyboard()
    except:
        pass

    print("Waiting 6 seconds for results...")
    time.sleep(6)
    
except Exception as e:
     print(f"Error typing: {e}")
     driver.quit()
     exit()

# --- Task 3: Handle 'Not Now' Pop-up (Conditional) ---
try:
    wait = WebDriverWait(driver, 5)
    not_now_btn = wait.until(EC.presence_of_element_located((
        AppiumBy.ID, 
        "com.flipkart.android:id/not_now_button"
    )))
    not_now_btn.click()
    print("Clicked 'NOT NOW' on notification pop-up")
    time.sleep(2)
except:
    print("Notification pop-up did not appear. Proceeding...")

# --- Task 4: Click Product (UPDATED LOCATOR) ---
print("Selecting the product...")
try:
    # UPDATED BOUNDS: [0,1250][540,1898] and class android.widget.ImageView
    wait = WebDriverWait(driver, 10)
    
    # Using specific class ImageView with the new bounds
    product_image = wait.until(EC.presence_of_element_located((
        AppiumBy.XPATH, 
        '//android.widget.ImageView[@bounds="[0,1250][540,1898]"]'
    )))
    product_image.click()
    print("Clicked on the product successfully")
    time.sleep(6) # Wait for details page
    
except Exception as e:
    print(f"Error clicking product: {e}")
    driver.quit()
    exit()

# --- Task 5: Click 'Add to Cart' ---
print("Attempting to Add to Cart...")
try:
    # Using bounds [45,2228][527,2338]
    wait = WebDriverWait(driver, 10)
    action_button = wait.until(EC.presence_of_element_located((
        AppiumBy.XPATH, 
        '//*[@bounds="[45,2228][527,2338]"]'
    )))
    action_button.click()
    print("Clicked 'Add to Cart'")
    
    print("Waiting 8 seconds for button update...")
    time.sleep(8) 
    
except Exception as e:
    print(f"Error clicking Add to Cart: {e}")

# --- Task 6: Click 'Go to Cart' ---
print("Attempting to click 'Go to Cart'...")
try:
    # Clicking the SAME bounds again
    go_to_cart_btn = driver.find_element(
        AppiumBy.XPATH, 
        '//*[@bounds="[45,2228][527,2338]"]'
    )
    go_to_cart_btn.click()
    print("Clicked 'Go to Cart' successfully")
    time.sleep(5) 
    
except Exception as e:
    print(f"Bounds click failed for Go to Cart. Trying text fallback...")
    try:
        go_to_cart_text = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 
            'new UiSelector().textContains("GO TO CART")'
        )
        go_to_cart_text.click()
        print("Clicked 'Go to Cart' using Text")
    except Exception as e2:
         print(f"Could not find Go to Cart button: {e2}")

# --- End ---
print("Script finished.")
# driver.quit()