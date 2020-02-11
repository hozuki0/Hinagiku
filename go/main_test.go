package main

import (
	"testing"
)

func TestBanishMessage(t *testing.T) {
	if !isBanishMsg("消えろ") {
		t.Fatal("failed test banish message 消えろ is banish message")
	}
	if !isBanishMsg("失せろ") {
		t.Fatal("failed test banish message 失せろ is banish message")
	}
}
