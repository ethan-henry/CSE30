Purpose: The purpose of this program is to attempt to keep track of people following SD6 using Computer Vision.

Use: Click the ESC button to stop the program. Otherwise, if a video is provided, the program will stop at the end of the video

Special: I used a method that seeks out movemnt first.  After found, the moving object is run through a method that attempts to classify the
object using a Haar Cascade model.  The breaking of SD6 is considere to be whenever 2 moving objects are close enough to merge thier bounding boxes
and there is more than one human within that box.

Outputs: The Output of the program is 1 of 3 texts.  The first, following SD6 means that there is around a 25% chance that people are not following SD6 
and 75% chance they are.  Probably not following SD6 means there is around a 75% chance that people are not following SD6 and a 25% chance that people 
are following SD6.  Lastly, there is not following SD6, which means there is a 100% chance that someone is breaking SD6 and 0% chance that people are following
SD6.