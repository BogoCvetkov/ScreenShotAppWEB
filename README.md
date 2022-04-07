<h1 align="center">
  <br>
  <img src="https://res.cloudinary.com/dawb3psft/image/upload/v1649261206/Portfolio/ad_capture.png" alt="AdCaptureBot" width="300">
</h1>

<h4 align="center">Web App for automated monitoring of competitor's Facebook ads.</h4>

<p align="center">
  <a href="https://img.shields.io/badge/Made%20with-Python-blue">
    <img src="https://img.shields.io/badge/Made%20with-Python-blue"
         alt="Gitter">
  </a>
  <a href="https://img.shields.io/badge/Made%20with-JavaScript-yellow">
    <img src="https://img.shields.io/badge/Made%20with-JavaScript-yellow"></a>
  <a href="https://img.shields.io/tokei/lines/github/Bogo56/AdCapture_bot">
      <img src="https://img.shields.io/tokei/lines/github/Bogo56/AdCapture_bot">
  </a>
  <a href="https://img.shields.io/github/languages/count/Bogo56/AdCapture_bot?color=f">
    <img src="https://img.shields.io/github/languages/count/Bogo56/AdCapture_bot?color=f">
  </a>
  <a href="https://badgen.net/github/commits/Bogo56/AdCapture_bot">
    <img src="https://badgen.net/github/commits/Bogo56/AdCapture_bot">
  </a>
</p>

<p align="center">
  <a href="#about-the-project">About The Project</a> •
   <a href="#so-why-the-same-app-again">So why the same app again?</a> •
  <a href="#description-of-the-problem">Description of the problem</a> •
  <a href="#project-workflow">Project Workflow</a> •
  <a href="#project-structure">Project Structure</a> 
  
</p>

## Built With
###  Languages
<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  
<p>
  
### Frameworks
<p>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
</p>

### Databases
<p>
<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
<img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white">
</p>

### Additional Libraries and Technologies
<p>
  <img src="https://img.shields.io/badge/ORM-SQLALCHEMY-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Migrations-Alembic-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/TEMPLATING-JINJA-9cf?style=for-the-badge">
  <img src="https://img.shields.io/badge/serialization-marshmallow-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/OS-UBUNTU-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/ASYNC-RQ-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/WebAutomation-Selenium-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Security-Bcrypt-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Security-JWT-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/SCHEDULING-APSCHEDULER-important?style=for-the-badge">
   <img src="https://img.shields.io/badge/+-To be continued-blueviolet?style=for-the-badge">
 
</p>

## About The Project
*This is a work-in-progress project. I'm almost done with the backend part(3.5 months), but still some of the ideas and techologies have not yet been implemented. Soon I'll start working on the frontend and hopefully it will be ready in about a month🤞.

This web app is the natural evolution of a previous more simple native app that I have created for my team,  inspired by a **REAL-world scenario**, that we **had at the company** (Digital-Marketing company) I'm working at. 
You can check that app here if you're curious: https://github.com/BogoCvetkov/AdCapture_bot

## So why the same app again
During the first month of it's usage in my team I managed to get a lot of feedback about the flaws of the first app. It was not as intuitive to use, it was harder to maintain and also it didn't provide the level of automation that it was created for. Still it turn out to provide value for the company and our clients, so I decided it's time to get serious about it and create a REAL app, that could scale better and really achieve it's goal of delivering automation. An app that could actually be sold as a service.

FLAWS OF THE OLD APP:
- it was a native python-kivy app - which made it difficult for distribution every time it needed to be updated or fixed - quite often actually😅
- everyone had to unzip the app on their computers - it was not an integrated shared environment, where everyone had access to the same resources.
- it was not a real automation - because you had to open it and click 2 or 3 buttons to activate the flow - which would not scalable at all for a lot of clients

HOW WILL THIS APP BE BETTER:
- first it's going to be a web-based app - this significantly would improve the maintainability, accessibility and scalability issues
- the architecture and design of the app is inspired by Facebook Ads Manager - something all of my teammates(+ME) are using on a daily basis. So it should feel much more intuitive and familiar.
- as any REAL app it includes access management
- the app itself will be an unified shared environment, that contains all the resources in itself. Users (my teammates) will just be accessing those resources after authentication. Meaning that multiple people could manage and modify the same resource. This is the way Facebook generally designes it's platform, so I really wanted to stay close to that idea. Also this would make the learning curve much less steeper.
- it will achieve real automation and hopefully a degree of stability - it will run on a server, with background workers active 24/7. So my colleagues will only have to configure and schedule the particular jobs once and leave the rest to the bots
- this solution will be scalable as well because it's a set once operation - meaning adding more and more accounts, will not result in more time consumed for the team.

I can really write a lot more about this app , the idea, the multiple challenges that I've faced, how I solved them etc. But this would get quite long, so I leave it at that.😅

## Description of the problem
So basically Facebook has a section - (https://www.facebook.com/ads/library) - where anyone can see if a certain page currently has active ads and what they are. You can also filter your search by category, keywords, countries etc. A lot of times we needed to manually visit the page, make multiple screenshots for different competitors that a client has and then collect all those screenshots and send them on email to the client. Sometimes this was done a couple of times a week - loosing about 2-3 hours of productive time per person per month.

### And the Solution
I wanted to create a solution that would be usefull to all my teammates and not just myself. That's why a simple script was not enough. So i had to create an app that **could be used by anyone and mainly non-coders**. This is how I came up with this project. It basically visits every competitor, scrolls trough all the ads, makes a screenshot, generates a PDF from all screenshots in the end and sends it on email.

## Project Workflow
Here, I'm outlining very briefly the phases that the project went trough from start to finish.

### Phase 1 - Restructuring
I already had the core functionality from the earlier app. Now  I had to readapt and recreate everything else and turn it into a web-based solution. So I Restructured the project and left only the critical parts that were working well
  
### Phase 2 - Creating the database structure, taking care of migrations and integrating SQLAlchemy as ORM
Here I have spend a lot of time in researching how to properly structure the database and model the data, how to handle migrations and how to properly use the rich functionalities that SQLAlchemy offers as an ORM.

### Phase 3 - Creating an API for managing resources and accessing the service itself
Now I had to really transform this app into a web-based one. I created an API that would be consumed by the Frontend, where the user will actually controll the whole flow.

### Phase 4 - User Management and Authentication
Since this is an app intended only to be used internally inside the company, I had to restrict the access to it. I'm using JWT tokens for that purpouse. All passwords are hashed. There would also be some endpoints accessible only for particular roles etc. There are still other things that I plan to implement to enhance security.

### Phase 5 - Async - offloading time consuming tasks to background workers
The challenge here was taking care of time-consuming operations - taking screenshots and sending emails should not block the main tread - were requests are being handled. So after a lenghtly research I decided to use task queues and background workers that would execute the jobs in the background.

### Phase 6 - Taking care of multi-threading
Since I have a total of 4 workers running and all of them are accessing the same resources,this means it's quite possible that more than one worker tries to modify the same file at the same time. This is my first time dealing with multi-threading scenarios. So I've spent about two weeks researching and developing a mechanism by which the workers would communicate and synchronise the operations between themselves so that two important conditions are always being met:
- priority jobs(jobs in the schedule queue) are always being executed - and all other queues that have the same job won't execute it
- save server resources - if the job was already done or is currently being done, skip it in the other workers - stay DRY

### Phase 7 - Creating the schedule script that will run as a separate daemon process on the server
This script runs on the background constantly monitoring the scheduled jobs and when the time comes it sends them to the respective task queue to be executed by the workers.

### Phase 8 - Taking care of the Frontend - Not yet ready

## Project Structure
```
📦 ScreenShotAppWEB
├─ .gitignore
├─ Project
│  |
│  ├─ alembic.ini
│  ├─ alembic
│  │  ├─ env.py
│  │  ├─ script.py.mako
│  │  └─ versions
│  │     ├─ 22e61dc73dc0_add_last_operation_date_in_accounts_.py
│  │     ├─ 28736d0b84e3_add_account_table.py
│  │     ├─ 360776d91d7a_add_table_for_password_reset_token.py
│  │     ├─ 47b9c1118ca4_add_account_page_index.py
│  │     ├─ 6a70d4f336c0_create_schedules_table.py
│  │     ├─ 6c589bf489b8_add_last_changed_column_to_user.py
│  │     ├─ 77f1d7fab661_create_a_table_for_pdf_screenshots_with_.py
│  │     ├─ 93eb863789cf_add_pages_table.py
│  │     ├─ a59d2adf71b1_make_account_name_unique.py
│  │     ├─ bc799c6d0d13_add_logs_table.py
│  │     └─ c76339936dc9_add_user_table.py
│  ├─ app
│  │  ├─ Async
│  │  │  ├─ callbacks.py
│  │  │  ├─ jobs
│  │  │  │  ├─ clean_up.py
│  │  │  │  ├─ make_screenshot.py
│  │  │  │  ├─ scheduled_emails.py
│  │  │  │  └─ send_emails.py
│  │  │  ├─ queues.py
│  │  │  ├─ redis_conn.py
│  │  │  ├─ spawn.txt
│  │  │  └─ workers
│  │  │     ├─ client_worker.py
│  │  │     └─ kill_all.py
│  │  ├─ app.py
│  │  ├─ auth
│  │  │  ├─ jwt.py
│  │  │  └─ security.py
│  │  ├─ controller
│  │  │  ├─ account_controller.py
│  │  │  ├─ auth_controller.py
│  │  │  ├─ controller_factory.py
│  │  │  ├─ me_controller.py
│  │  │  ├─ page_controller.py
│  │  │  ├─ schedule_controller.py
│  │  │  ├─ service_controller.py
│  │  │  └─ user_controller.py
│  │  ├─ routes
│  │  │  ├─ all_routes.py
│  │  │  └─ api
│  │  │     ├─ account_route.py
│  │  │     ├─ auth_route.py
│  │  │     ├─ me_route.py
│  │  │     ├─ page_route.py
│  │  │     ├─ schedule_route.py
│  │  │     ├─ service_route.py
│  │  │     └─ user_route.py
│  │  └─ schemas
│  │     ├─ account_schema.py
│  │     ├─ auth_schema.py
│  │     ├─ page_schema.py
│  │     ├─ schedule_schema.py
│  │     └─ user_chema.py
│  ├─ config.py
│  ├─ errors
│  │  ├─ custom_errors.py
│  │  └─ handler.py
│  ├─ model
│  │  ├─ DB.py
│  │  ├─ account_model.py
│  │  ├─ all_models.py
│  │  ├─ common
│  │  │  └─ base_mixin.py
│  │  ├─ features
│  │  │  └─ searching.py
│  │  ├─ logs_model.py
│  │  ├─ page_model.py
│  │  ├─ reset_pass_model.py
│  │  ├─ schedule_model.py
│  │  ├─ screenshot_model.py
│  │  └─ user_model.py
│  ├─ scripts
│  │  └─ schedules.py
│  ├─ server.py
│  └─ service
│     ├─ bots
│     │  ├─ __init__.py
│     │  ├─ base.py
│     │  ├─ capture_bot.py
│     │  └─ send_bot.py
│     ├─ scraper
│     │  ├─ ad_capture.py
│     │  └─ web_driver.py
│     └─ utils
│        ├─ dir_maker.py
│        ├─ email_sender.py
│        └─ to_pdf.py
└─ README.md
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)
