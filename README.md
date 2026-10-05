hello
im learning python a little bit

problems
1. when a song in the queue finishes it doesn't get removed from the queue
2. does the pygame queue only store 1 song? it does.

solution
- implement own queue functionality. plays next song in queue when song finishes. only removes the song in the queue if it was the song that actually started playing.
- make custom pygame user event, when song sends, first check if this song was played from the queue. check if it's in 0 pos of queue, if then remove it. then check for next song. play it if there is. if it isn't there return to the home menu.
