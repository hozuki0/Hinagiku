package utility

import "time"

// DelayFunction ...
func DelayFunction(f func(), delaySec time.Duration) {
	go func() {
		t := time.NewTicker(delaySec * time.Second)
		for {
			<-t.C
			f()
			break
		}
		t.Stop()
	}()
}
