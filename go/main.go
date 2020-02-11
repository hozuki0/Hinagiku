package main

import (
	"fmt"
	"github.com/bwmarrin/discordgo"
	"io/ioutil"
	"log"
	"strings"
)

var stopBot = make(chan bool)

type Mode int

const (
	Normal Mode = iota
	Banish
	Dice
	Gerotter
)

var isDebug = true

func main() {
	token, err := readTokenFile("../token.tk")
	if err != nil {
		fmt.Println(err)
	}

	discord, err := discordgo.New()
	if err != nil {
		fmt.Println(err)
	}
	discord.Token = "Bot " + token

	discord.AddHandler(onMessageCreate)

	err = discord.Open()
	if err != nil {
		fmt.Println(err)
		return
	}
	<-stopBot

	return
}

func readTokenFile(path string) (string, error) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(data)), nil
}

func onMessageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {
	c, err := s.State.Channel(m.ChannelID)
	if err != nil {
		log.Println("Error getting channel:", err)
	}
	if isBotMessage(m) {
		return
	}
	if canSendMsg(c.Name) {
		if m.Content == "消えろ" {
			sendMessage(s, c, "自害下UD :ud:")
			stopBot <- true
			return
		}
		sendMessage(s, c, "Yuppi☆")
	}
}

func sendMessage(s *discordgo.Session, c *discordgo.Channel, msg string) {
	_, err := s.ChannelMessageSend(c.ID, msg)

	log.Println(">>> " + msg)
	if err != nil {
		log.Println("Error sending message: ", err)
	}
}

func isBotMessage(m *discordgo.MessageCreate) bool {
	return m.Author.Bot
}

func decideMode(msg string) Mode {
	if isBanishMsg(msg) {
		return Banish
	}
	return Normal
}

func isBanishMsg(msg string) bool {
	if strings.Contains(msg, "消えろ") || strings.Contains(msg, "きえろ") {
		return true
	}
	if strings.Contains(msg, "失せろ") || strings.Contains(msg, "うせろ") {
		return true
	}
	return false
}

func canSendMsg(channelName string) bool {
	if isDebug && channelName == "yuppibot-debug" {
		return true
	}
	return false
}
