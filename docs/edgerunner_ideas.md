# Ideas for edgerunner-pomodoro

1. Add meetings to your work schedule, configure aletrs, the timer will display them both in the interface and as a popup.

1. Completely configurable environment (colors, font sizes, button placement, sounds, messages). Maybe should create a huge config file for that.

1. CLI version to run in a terminal. Fullscreen with visual countdown line and colored text, TMUX size, 40-character and 80-character mode for nerds.

* Share timer settings between GUI and CLI versions

## Countdown loop termination status detection

How do you tell the loop it's over not because we clicked **Stop**, but because the timer has run out?

As of yet, we've got the trigger disabling the `countdown` loop as soon as the buffer runs down to `0`. We need another way to tell if the change to zero was natural (the timer has run out) or deliberate (clicked **Stop**).

The one way I see it don is by breating a boolean variable named something like `StopDeliberate` and go for the following logic:

* `TRUE` if we actually clicked **Stop** and halted the `countdown` loop ourselves. Then it won't automatically engage the following timer period.

* `FALSE` if the loop interrupt occurred procedurally, os we need to engage the script to start the following time period automatically.
