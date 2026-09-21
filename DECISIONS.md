# Decision log

---

## 1. What did you set out to build, and what changed?

I am currently writing this at the very start of the project. I am wanting to make a page of all my present and previous hobbies. Now I am going to have a page per hobby instead of just having one page. I think this will allow for more creativity in the long run. Other than that I did what I set out to build and did not change too much.

---

## 2. A fork in the road

I found a fork in the road when I was deciding on multiple pages or 1. As of now I decided on 1 page in order to keep the UI more simple and easier to navigate. However, this means that I won't be able to have as much information on all my hobbies. I decided to switch to a main page and then having links to each of my hobbies on separate pages. This allows for more creativity on each page. I was wondering if I should add videos or not and decided it was worth it. This allows for more expression, a photo is 1000 words but a video is much more. However, this will make the pages more clunky looking and not formatted the exact way I would want it. I did not want to use Javascript originally but I decided to change the photo format from a grid to a clickable view of the photos. Claude suggested this would be easiest in JavaScript so I accepted as it is always revertable. I made this decision because having a grid of 20+ photos is hard to look at and the click through option should help the user see everything better. 

---

## 3. Where you overruled the agent

I was working in planning mode and Claude suggested deleting some of my hobbies to make the page easier to read. I did not agree to this and ended up keeping all my hobbies but switched to multiple pages to make it so I could keep them all. Claude wanted to just make the heading blue when I wanted the whole website to be blue and white themed. I reviewed my plan and had to get all the text to be blue with the background white. The agent gave me duplicate images and captions when loading up a specific page, I changed this to only have 1 image. Also, the heading for the page was below the images, I wanted it to be above them. I asked claude to tighten up the captions of my photos and it just made it into AI slop. I had to go back to my original wording. Also, there was poor arrow and image positioning for the page. Claude had the portrait images cut off in order for the arrows to stay in the same place. I saw this and changed it so the arrows snap on the side of the image so nothing gets cut off. I also changed the captions of the image to go center under the image instead of the left centered, and swapped the image count to be on the bottom left instead. 

---

## 4. How you know it works

[verification/](verification/) has the screenshot, the fetch output, and what I checked.

I chose to run a python script so the site stays HTML and CSS. I checked this by adding photos, confirming the grid rendered, and reran it to confirm it was repeatable. If the grid did not render then the script failed. I changed from a grid to a gallery and when changing that I made sure that the images and videos were uploaded properly and fully showed up. I also checked all of the links and buttons to make sure they took me to the correct location and swapped images/videos correctly. Lastly, I checked the main url for my site: https://hyrex8301.github.io. I made sure it was the new version of Main instead of the old showing all the finishing touches I added. The content section would have nothing if it did not update. I also did one last check of everything on the website by hand checking everything before turning it in. 

---

## 5. What is still wrong

I still think that the arrows on the sides of the images/videos are a little clunky. I would like to have them in a stationary area while still making it look good for portrait and landscape images. As of now it snaps to the edge of each but that makes it so you can't click super fast through all of the images. I would have users test it and see what works best for them. I of course will want to add more images and videos with more hobbies. That is most likely the first thing that I will do. 