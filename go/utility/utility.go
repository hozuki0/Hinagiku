package utility

import "time"

// DelayFunction ...
func DelayFunction(callback func(), delaySec time.Duration) {
	time.AfterFunc(delaySec*time.Second, callback)
}
