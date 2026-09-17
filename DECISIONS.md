# Decision log

---

## 1. What did you set out to build, and what changed?

I am currently writing this at the very start of the project. I am wanting to make a page of all my prresent and previos hobbies. Now I am going to have a page per hobbie instead of just having one page. I think this will allow for more creativity in the long run. 

---

## 2. A fork in the road

I found a fork in the road when I was deciding on multiple pages or 1. As of now I decided on 1 page in order to keep the UI more simple and easier to navigate. However, this means that I won't be able to have as much information on all my hobbies. I decided to switch to a main page and then having links to each of my hobbies on seperate pages. This allows for more creativity on each page. I was wondering if I should add videos or not and decided it was worth it. This allows for more expression, a photo is 1000 words but a video is much more. However, this will make the pages more clunky looking and not formated the exact way I would want it. I did not want to use Javascript originally but I decided to change the photo format from a grid to a clickable view of the photos. Claude suggested this would be easiest in JavaScript so I accepted as it is always revertable. I made this decision becuase having a grid of 20+ photos is hard to look at and the click through option should help the user see everything better. 

---

## 3. Where you overruled the agent

I was working in planning mode and Claude suggested deleting some of my hobbies to make the page easier to read. I did not agree to this and ended up keeping all my hobbies but switched to multiple pages to make it so I could keep them all. Claude wanted to just make the heading blue when I wanted the whole website to be blue and white themed. I reviewed my plan and had to get all the text to be blue with the background white. The agent gave me duplicate images and captions when loading up a specific page, I changed this to only have 1 image. Also, the heading for the page was below the images, I wanted it to be above them. I asked claude to tighten up the captions of my photos and it just made it into AI slop. I had to go back to my original wording. 

---

## 4. How you know it works

What check did you run, and what did it tell you?

Then the real question: **what would have made this check fail?**
A check that could not have failed is not a check.

Link to your `verification/` folder.

*Your answer here.*

I chose to run a python script so the site stays HTML and CSS. I checked this by adding photos, confirming the grid rendered, and reran it to confirm it was repeatable. 

---

## 5. What is still wrong

One thing on your own site that is not right, not finished, or that you do not
fully understand.

What would you do next, and how would you find out?

*Your answer here.*
