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

func TestIsXXXMessage(t *testing.T) {
	if !isXXXMsg("isRoR2") {
		t.Fatal("failed test isXXX message isRoR2 has 'is prefix'")
	}
	if !isXXXMsg("Is睡眠") {
		t.Fatal("failed test isXXX message Is睡眠 has 'Is prefix'")
	}
	if isXXXMsg("aaa") {
		t.Fatal("failed test isXXX message aaa has no 'is prefix'")
	}
	if isXXXMsg("aaais") {
		t.Fatal("failed test isXXX message aaais has no 'is prefix'")
	}
}

func TestCutMention(t *testing.T) {
	if cutMention("<@0000000000> aiueo") != "aiueo" {
		t.Fatal("faield to cutMention ")
	}
	if cutMention("aiueo") != "aiueo" {
		t.Fatal("faield to cutMention ")
	}
}
