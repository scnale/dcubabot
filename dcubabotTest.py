#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest

import json

import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater

from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import Mockbot
from ptbtest import UserGenerator

from dcubabot import start, estasvivo, help, listar


class TestDCUBABot(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # For use within the tests we nee some stuff. Starting with a Mockbot
        self.bot = Mockbot()
        self.bot.request = telegram.utils.request.Request()
        # Some generators for users and chats
        self.ug = UserGenerator()
        self.cg = ChatGenerator()
        # And a Messagegenerator and updater (for use with the bot.)
        self.mg = MessageGenerator(self.bot)
        self.updater = Updater(bot=self.bot)
        self.updater.dispatcher.add_handler(CommandHandler("help", help))
        self.updater.dispatcher.add_handler(CommandHandler("start", start))
        self.updater.dispatcher.add_handler(CommandHandler("estasvivo", estasvivo))
        self.updater.dispatcher.add_handler(CommandHandler("listar", listar))
        print("Hice setup")
        self.updater.start_polling()

    @classmethod
    def tearDownClass(self):
        self.updater.stop()

    @classmethod
    def sendCommand(self, command):
        user = self.ug.get_user(first_name="Test", last_name="The Bot")
        chat = self.cg.get_chat(user=user)
        update = self.mg.get_message(user=user, chat=chat, text=command)
        self.bot.insertUpdate(update)

    def test_help(self):
        self.sendCommand("/help")
        # self.assertEqual(len(self.bot.sent_messages), 1)
        sent = self.bot.sent_messages[-1]
        self.assertEqual(sent['method'], "sendMessage")
        self.assertEqual(sent['text'], "Yo tampoco sé qué puedo hacer.")

    def test_start(self):
        self.sendCommand("/start")
        # self.assertEqual(len(self.bot.sent_messages), 1)
        sent = self.bot.sent_messages[-1]
        self.assertEqual(sent['method'], "sendMessage")
        self.assertEqual(
            sent['text'], "Hola, ¿qué tal? ¡Mandame /help si no sabés qué puedo hacer!")

    def test_estasvivo(self):
        self.sendCommand("/estasvivo")
        # self.assertEqual(len(self.bot.sent_messages), 1)
        sent = self.bot.sent_messages[-1]
        self.assertEqual(sent['method'], "sendMessage")
        self.assertEqual(sent['text'], "Sí, estoy vivo.")

    def test_listar(self):
        self.sendCommand("/listar")
        # self.assertEqual(len(self.bot.sent_messages), 1)
        sent = self.bot.sent_messages[-1]
        self.assertEqual(sent['method'], "sendMessage")
        self.assertEqual(sent['text'], "Grupos: ")

        # Assertions on keyboard
        inline_keyboard = json.loads(sent['reply_markup'])['inline_keyboard']
        self.assertEqual(len(inline_keyboard), 2)  # Number of rows
        for i in range(2):
            row = inline_keyboard[i]
            self.assertEqual((len(row)), 3)  # Number of columns
            for j in range(3):
                button = row[j]
                button_number = str(i*len(row)+j)
                self.assertEqual(button['text'], "Texto " + button_number)
                self.assertEqual(button['url'], "https://url" + button_number + ".com")
                self.assertEqual(button['callback_data'], "data" + button_number)


if __name__ == '__main__':
    unittest.main()