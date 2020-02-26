package utility

import "time"

// DelayFunction 指定時間後に指定関数を実行する
func DelayFunction(callback func(), delaySec time.Duration) {
	time.AfterFunc(delaySec*time.Second, callback)
}
