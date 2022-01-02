# 計算理論 final project (Line bot with FSM)
by 梁華軒  2022/1/2
## Require ENV
Check the requirements.txt, although not all of them are require.
<br>Because I didn't clean the pip in my computer.  

## FSM (Maping state with GraphMachine)
![](https://i.imgur.com/4uEkba5.png)


## Introduction
### Add friend with the bot
Not thing will happend, unless you type any message.
<br>After sending message, you are enrolled in the geme.  
![](https://github.com/wilson20010327/line_bot_tennis/blob/main/static/enrol.jpg)

### Init
After enrol, you can play the game now.
<br>There are three buttons to type, 
* detail: for more information about the game
* start : for start playing the game
* 排行榜: for check the score list who have won the game before

![](https://github.com/wilson20010327/line_bot_tennis/blob/main/static/scorelist.jpg)

### User_serve
After start, you can decide where to serve
<br>There are three buttons to type,
* Left : for serving to left
* Rigth: for serving to right
* Score: for checking recent score

![](https://github.com/wilson20010327/line_bot_tennis/blob/main/static/serve.jpg)

### Lint bot defense
After User_serve, Lint bot can decide where to defense.
* If it guess in the right place, then you have to defense where it is going to serve.
* if not, you get the point and you can keep serving.


### User_defense
After line serve, you can decide where to defense
<br>There are three buttons to type,
* Left : for defensing to left
* Rigth: for defensing to right
* Score: for checking recent score
    * If you guess in the right place, then line bot have to defense where it is going to serve.
    * if not, line bot get the point and line bot can keep serving.

![](https://github.com/wilson20010327/line_bot_tennis/blob/main/static/defence_correct.jpg)![](https://github.com/wilson20010327/line_bot_tennis/blob/main/static/defence.jpg)!
### WIN or LOSE
Check whether score is bigger than the score max
<br>With different condition respone different image 

![](https://github.com/wilson20010327/line_bot_tennis/blob/main/static/win.jpg)![](https://github.com/wilson20010327/line_bot_tennis/blob/main/static/lose.jpg)

## Using in project
![](https://github.com/wilson20010327/line_bot_tennis/blob/main/static/python_line_bot_deploy_to_heroku.PNG)

[參考server](https://www.learncodewithmike.com/2020/07/python-line-bot-deploy-to-heroku.html)<br>
[參考database](https://ithelp.ithome.com.tw/articles/10239404)<br>
[參考爬蟲](https://www.learncodewithmike.com/2020/07/line-bot-buttons-template-message.html)<br>
[參考專案建設](https://www.learncodewithmike.com/2020/06/python-line-bot.html)
