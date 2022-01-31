from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import numpy
import random
from PIL import Image
import base64
import io




class Learn():
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=800,600")
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        options.add_argument("--log-level=3")
        options.add_argument("--mute-audio")
        #options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        while 1:
            try:
                driver = webdriver.Chrome( executable_path = './chromedriver.exe', chrome_options=options)
                break
            except:
                continue

        driver.get("https://dino-chrome.com/")
        self.size_x = 547
        self.size_y = 150
        driver.execute_script("document.getElementsByClassName('runner-canvas')[0].style = 'width:{}px;height:{}px;'".format(self.size_x,self.size_y))
        while driver.execute_script("return Runner.instance_.started") == False:
            actions = ActionChains(driver)
            actions.send_keys(Keys.SPACE).perform()


        
        self.driver = driver
        self.time_alive = time.time()
    def get_data(self):
        data = base64.b64decode(self.driver.execute_script('return document.getElementsByClassName("runner-canvas")[0].toDataURL("image/png").substring(21);'.format(self.size_x,self.size_y)))
        image = Image.open(io.BytesIO(data))
        

        y_pos = self.driver.execute_script("return Runner.instance_.tRex.yPos")

          #[start_x,end_x]

        #find cactuses
        
        obj = {36:[],50:[]}
        for b in [36,50]:
            obstacles = [] 
            open = False
            after = 100
            for i in range(90,self.size_x):
                pixel = image.getpixel((i,self.size_y-b))
                if pixel != (0,0,0,0) and not open:
                    if after >20:
                        obstacles.append([i])
                    open = True
                    after = 0
                else:
                    if open and  pixel == (0,0,0,0) and after > 20:
                        obstacles[-1].append(i)
                        open = False   
                    after +=1

            if len(obstacles) and len(obstacles[-1]) == 1:
                obstacles[-1].append(546)
            
            if len(obstacles) <2:
                r = 2-len(obstacles)
                for i in range(r):
                    obstacles.append([600,600])
            obj[b] = obstacles


        speed = self.driver.execute_script("return Runner.instance_.currentSpeed")

        data = [y_pos,speed,obj[36][0][0],obj[36][0][1],obj[36][1][0],obj[36][1][1], obj[50][0][0],obj[50][0][1],obj[50][1][0],obj[50][1][1]]
        return data

    def step(self,action):
        done = self.driver.execute_script("return Runner.instance_.crashed")
        self.time_alive = time.time()
        if self.driver.execute_script("return Runner.instance_.paused "):
            self.driver.execute_script(" Runner.instance_.play() ")
        if action[0] > 0:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.SPACE).perform()
    
        return done

    def end(self):
        data = int(''.join(self.driver.execute_script('return Runner.instance_.distanceMeter.highScore')[2::]))
        self.driver.close()
        return data 



