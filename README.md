# Report Generator - Web Application
#### Video Demo: 
#### Description: 
> ##### CS50 Final Project by H.M.R.Vimarshana Herath
> WEB URL: http://ReportGenerator101.pythonanywhere.com

### Introduction
> Sometimes we prepare ***Budget Reports*** for simple events we do in day-to-day life using installed software in our computer. For a simple task like this we won't install editing softwares and converting softwares in future. Storing files everywhere on your local system mess up your mind. Don't miss any file! This is the best solution!! ***Report Generator*** keeps all your financial data on different projects or events as it is always accessible by login into your account from any device. With a one click, you can download it as a **PDF report** and share as you own. Simply delete the **PDF** after sharing. We have everything about your report. Simple download it again.

### Usage

>1. Register as a user
- In register tab fill all details correctly.
- We ask for a User Name, Email, Password, Password Confirmation, Contact No and all inputs are confirmed by js.
- If User Name it is already exists, web page returns without registering the user with Error Message.
- If user input invalid email, system will return with error message.
- Contact Number length must be 10 digits. If user input wrong Number system will return with error message. 
    
    +    After register as a user system will logged you into application

>2. Create New Report related to project
- By hitting on ***New Report*** tab you can create New Project
- Include all the details necessary.
- You can give anything as a category it will sort projects on category wise on your profile. So specifying a category will group your projects. 
- Add starting and ending date of your project. It will use as duration of your project as well as report
- Add a brief description of your project and click proceed. It will create a new record of your project and you will redirect to Dashboard.
- In there you can see all your projects

>3. Inserting new financial records
- By clicking ***See More*** in every project palette you will redirect to **project details** page.
- In there you can see project name, project id and category and starting/ending dates as well as description.
- By clicking on ***Add Expenditure or Income** page will return form.
- First, choose what you enter as it is income or expenditure.
- Then add a category as you wish and in *Input Item* you can provide description of record.
- Set resulting date of that record.
- Total amount is calculated on (units)\*(unit Amount). So if user leave *units* it as blank system will automatically use default value as 1.
- After clicking ***save*** it will preview on tables.
- If user want to delete some record, click on ***DEL***. After confirmation, it will completely delete your record. The result can never undo.

>4. Generating PDF
- Whenever user want to generate pdf click on **Generate PDF**. It will prompt PDF settings.
- User can select page orientation, paper size and font size. 
- User can provide report label if want.
- No matter to keep all fields empty and click ***Generate***, it will use default settings to generate pdf.

>5. Delete Project
- Go to profile, there user can delete their projects by clicking ***DEL***.

### Overview
[![python](https://www.python.org/static/community_logos/python-powered-w-140x56.png)](https://docs.python.org/3/)

***Report Generator*** is built using *Flask* framework power by python.

Front-End developed using **HTML** and **JS**

+ Back-End uses different libraries
1. Flask
2. flask_session
3. cs50
4. random
5. werkzeug.security
6. os
7. shutil

+ There are 4 python scripts in use when running application.
1. app.py ***main script***
    + app.py contains main script of application. This contains 7 routes.
2. helper.py
    + contains Wrapper-loging_required function
3. report_generator.py
    - This file contains generate_pdf_report object and it initialize all properties of PDF. budget_report function in that object create PDF file.
4. User.py
    - This file contains user object. It validates and initialize new user.

+ In static directory
1. img folder for images
2. style folder for stylesheets
3. script folder for js files
4. reports folder to tempararily store user generated reports

+ In templates directory we store all the web pages
+ manager.db in main directory refers sqlite3 database use to store data.
    - Database consist with 4 created tables and 1 auto-created table.


