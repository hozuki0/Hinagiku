package main

import (
	crand "crypto/rand"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"math/big"
	"math/rand"
	"strings"

	"github.com/Hinagiku/go/utility"
	"github.com/bwmarrin/discordgo"

	"github.com/seehuhn/mt19937"
)

var (
	stopBot                            = make(chan bool)
	isDebug                            = true
	isBanished                         = false
	myName                             = "Yuppi☆"
	timerMessageChannelName            = "yuppibot-debug"
	prolabServerGuildID                = "527871282646220830"
	random                  *rand.Rand = nil
)

type Mode int

const (
	Normal Mode = iota
	Banish
	Dice
	Gerotter
)

func main() {
	seed, _ := crand.Int(crand.Reader, big.NewInt(math.MaxInt64))
	rand := rand.New(mt19937.New())
	rand.Seed(seed.Int64())

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
	guild, err := discord.Guild(prolabServerGuildID)
	if err != nil {
		fmt.Println(err)
	}
	defer discord.Close()
	var timerMessageChannel *discordgo.Channel = nil
	for _, channel := range guild.Channels {
		if channel.Name == timerMessageChannelName {
			timerMessageChannel = channel
			break
		}
	}

	// timer event
	go func(d *discordgo.Session, c *discordgo.Channel) {
		timerUpdate(d, c)
	}(discord, timerMessageChannel)
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
	if isBotMessage(m) || isBanished {
		return
	}
	if canSendMsg(c.Name) && isMentionedToMe(m) {
		contentWithoutMention := cutMention(m.Content)

		if isBanishMsg(contentWithoutMention) {
			dead := func() {
				sendMessage(s, c, "自害下UD")
				stopBot <- true
			}
			preDead := func() {
				utility.DelayFunction(dead, 3)
				sendMessage(s, c, packMentionAndMessage("ｱｱｯ...", m.Author))
				isBanished = true
			}
			utility.DelayFunction(preDead, 1)

			return
		} else if isXXXMsg(contentWithoutMention) {
			sendMessage(s, c, m.Author.Mention()+" "+isXXX(m.Content))
			return
		}
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

func isXXXMsg(msg string) bool {
	return strings.HasPrefix(msg, "is") || strings.HasPrefix(msg, "Is")
}

func canSendMsg(channelName string) bool {
	if isDebug || channelName == "yuppibot-debug" {
		return true
	}
	return false
}

func isMentionedToMe(m *discordgo.MessageCreate) bool {
	for _, member := range m.Mentions {
		if member.Username == myName {
			return true
		}
	}
	return false
}

func timerUpdate(d *discordgo.Session, c *discordgo.Channel) {
	for !isBanished {
		// sendMessage(d, c, "ok!")

		break
	}
}

func diceRoll(msg string) int {
	return 0
}

func isXXX(msg string) string {
	if rand.Int()%2 == 0 {
		return "return true!"
	} else {
		return "return false!"
	}
}

func cutMention(msgWithMention string) string {
	if strings.HasPrefix(msgWithMention, "<@") {
		return strings.TrimSpace(msgWithMention[strings.Index(msgWithMention, "> ")+1:])
	}
	return msgWithMention
}

func cutMessage(msgWithMention string) string {
	if strings.HasPrefix(msgWithMention, "<@") {
		return msgWithMention[:strings.Index(msgWithMention, "> ")+1]
	}
	return msgWithMention
}

func packMentionAndMessage(msg string, user *discordgo.User) string {
	return user.Mention() + " " + msg
}
