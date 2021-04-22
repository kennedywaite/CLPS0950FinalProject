Brown University CLPS0950 Final Project

An exploratory project for Python’s TKinter graphical user interface package. Written by Ashley (Wen) Yuan, Bryan (Seong Wook) Park, Kennedy Waite, Erik Chen (The Running Brunonians Group). Submitted 22APR2021.

Title: The Netflix Organizer!

Abstract: Our project aims to explore the Python GUI package TKinter and use it to create a series of windows and buttons which we can then use to organize Netflix shows into certain categories. We pulled Netflix shows from a large .csv file which compiled nearly 8,000 distinct Netflix titles across various regions and genres, showcasing a wide array of directors and actors. The link to that spreadsheet can be found in our Github repository and is also linked here for downloading.

Instructions: From main.py, run the code. A small menu should appear with a start button to prompt the user to begin the program. From there, users can choose from Netflix shows sorted by ‘Genres’, ‘Country’, ‘Year Released’, and ‘Director’. If the user changes their mind and decides that they no longer want to procrastinate with Netflix, they can opt to go back to the start menu and quit.

After clicking on a category, say ‘Genres’, the user can then click on one of the menu options. Within the ‘Genres’ menu, all of Netflix’s show genres are listed to choose from. After clicking on one or more genre options, the user then clicks on either the ‘Inclusive’ or ‘Exclusive’ buttons. ‘Exclusive’ will generate 10 (or fewer) random shows from the list of shows which contain ALL genre tags selected by the user. ‘Inclusive’ will generate 10 (or fewer) random shows from a list of shows from ALL genre tags selected by the user. The randomly generated list is meant to symbolize the initial recommendation to a user as the program obviously does not collect any user data and there is no way for us to build a more tailored recommendation list. If a user is not happy with the list of shows displayed, hitting the ‘Inclusive’ or ‘Exclusive’ buttons will reroll a new list of 10 shows. Other categories have an ‘OK’ button, which will generate a list of shows from each selected menu option within each category. Included in each category is also a ‘Refresh’ button. This simply moves the displayed page to the next page for particularly long categories (like the list of publish years). If a user wants to start over with a new category, the quit button will close the program out and the user can start again. 

Once the user has selected a show that they are interested in, clicking on the title will pull up a brief blurb that summarizes all of the key points about the show, to include the description provided by Netflix.

File Descriptions:
Main.py -  the main program. Run this file to see how our program runs. It makes use of a number of defined functions which successively take genre inputs and creates buttons for the user to click through tkinter. There are multiple different page classes for each category (genre, country, year released, and director), and each page class has similar functions that create buttons and brings up the necessary information when buttons are pressed. Then, category_extraction is run at the bottom for all necessary categories, in order to use these variables throughout the Tkinter pages. 
Genre_extraction.py - extracts the various categories out of the .csv file which contains the raw information.
Keyword_extraction.py - test run using Python’s natural language toolkit which was ultimately scrapped in favor of using for/if loops to process the data set manually. 
Button_test.py - Testing tkinter and button creation to allow for streamlined button implementation into the main project file, using genres as a base case and testing it for other categories.
Textbox_test.py - Scrapped idea which took in user-inputted text. Opted for a button GUI instead.
User_input.py - Another scrapped idea which prompted users to log in/register. The idea was to create a user matrix that could take in ratings of Netflix titles from the user and calculate a similarity score between users. But, we wanted to focus on the basic organization of the Netflix titles. 
