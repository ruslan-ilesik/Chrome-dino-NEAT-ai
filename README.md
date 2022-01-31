# Chrome-dino-NEAT-ai
AI to play chrome dino game wrote on python, based on NEAT alghoritm

yotube video: https://youtu.be/pXsqaGeuyKE

1) install dependences from [dependences.txt](https://github.com/ruslan-ilesik/Chrome-dino-NEAT-ai/blob/main/dependences.txt)
2) download chromedriver based on your os and chrome version from [offical website](https://chromedriver.chromium.org/) and put file in "src" folder
3) Go to [./src/ai/learn.py](https://github.com/ruslan-ilesik/Chrome-dino-NEAT-ai/blob/main/src/ai/learn.py) and edit executable)path parameter in line 26 to your chromedriver filename
4) if you want you can edit [config](https://github.com/ruslan-ilesik/Chrome-dino-NEAT-ai/blob/main/src/ai/config) file
5) start an ai

There is an auto saving alghoritm which save population every 50 generations. You can get winner running only one generation. To replay winner use replay_genome (commented file in main.py)
