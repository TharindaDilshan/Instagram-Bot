from selenium import webdriver
from time import sleep

class Bot:
    def __init__(self, username, password):

        # Login using username and password
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(3)
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        sleep(1)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
    
    # Get usernames of followers not following back

    def getUnfollowers(self):
        # Go to profile after logging in. Use xpath to find the username to click
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        sleep(3)

        # Open following popup
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        sleep(2)
        following = self._generateNameList()

        # Open followers popup
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        sleep(2)
        followers = self._generateNameList()

        # Get the list of non followers by comparing following and followers lists
        nonFollowers = [user for user in following if user not in followers]
        print(nonFollowers)

    # Lists the names of followers and following
    def _generateNameList(self):
        # Access the scroll list using xpath
        scroll = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        # Heights of the scroll lists are compared to scroll until the end of the list
        # timer is set for 2s between each scroll to make the list load
        scrollHeightInitial, scrollHeightFinal = 0, 1
        while scrollHeightInitial != scrollHeightFinal:
            scrollHeightInitial = scrollHeightFinal
            sleep(2)
            scrollHeightFinal = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll)
    
        # anchor tags are seperated asusernames are wrapped inside anchor tags 
        # A list of names is created if the anchor tag contains text
        links = scroll.find_elements_by_tag_name('a')
        usernames = [name.text for name in links if name.text != '']

        # Close button for popup
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()

        return usernames
    
    def bulkLiker(self):
        self.driver.find_element_by_xpath("//a[@href = '/explore/']").click()
        sleep(4)
        self.driver.find_element_by_xpath("//a[contains(@href,'/p/')]").click()
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()
        sleep(2)
        for i in range(1000):
            self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]").click()
            sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()
            sleep(2)
        


        

# Username and password should be passed when creating an instancce of the class bot

# unfollowerBot = Bot('tharinda_dilshan97', '')
# unfollowerBot.getUnfollowers()

likerBot = Bot('tharinda_dilshan97', '')
likerBot.bulkLiker()
