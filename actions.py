# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import json
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dbConnect import getData
from inputAnalysis import productNameAnalysis
from inputAnalysis import romramAnalysis
from inputAnalysis import priceAnalysis


class ActionAnswerPrice(Action):
    def name(self) -> Text:
        return "action_answer_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name_input = tracker.get_slot('product_name')
        # price_input = tracker.get_slot('price')
        ram_input = tracker.get_slot('ram')
        rom_input = tracker.get_slot('rom')
        if product_name_input:
            productName = productNameAnalysis(product_name_input)
            query = "select * from TGDD.GiaDienThoai where ten like '%"+productName+"%'"
            '''
        if ram_input:
            ram = romramAnalysis(ram_input)
            query = query + "and ram like '%"+ram+"%'"
        if rom_input:
            rom = romramAnalysis(rom_input)
            query = query + "and rom like '%"+rom+"%'"
            '''
        # if price_input:
        #     price = priceAnalysis(price_input)
        #     query = query + "and gia like '%"+price+"%'"
        query = query + ";"
        data = getData(query)
        if data:
            ten = str(data[0]['ten']).strip("\n")
            gia = str(data[0]['gia']).strip("\n")
            response_message = "Giá của sản phẩm {} là: {}".format(ten,gia)
        else:
            response_message = "Rtất tiếc chúng tôi chưa hỗ  trợ sản phẩm này"

        dispatcher.utter_message(response_message)
        print("chạy action_answer_price")
        return

class ActionListProduct(Action):
    def name(self) -> Text:
        return "action_list_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone_company = getData("select * from TGDD.HangDienThoai")
        template_items = []
        for item in phone_company:
            payload = "Danh sách sản phẩm của " + item['ten']
            template_item = {
                "title": item['ten'],
                "image_url": item['url_logo'],
                "subtitle": "",
                "default_action": {
                    "type": "web_url",
                    "url": item['url_logo'],
                    "webview_height_ratio": "full"
                },
                "buttons": [
                    {
                        "type":"postback",
                        "title":item['ten'],
                        "payload":payload
                    }
                ]
            }
            template_items.append(template_item)

        message_str = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": template_items

                }
            }
        }
        ret_text = "Hi! You can choose from below items:"
        # print(message_str)
        dispatcher.utter_message(text=ret_text, json_message=message_str)
        print("chạy action_list_product")
        return

class ActionProductInfor(Action):
    def name(self) -> Text:
        return "action_product_infor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name_input = tracker.get_slot('product_name')
        if product_name_input:
            product_name = productNameAnalysis(product_name_input)
            query = "select * from TGDD.DienThoai where ten like '%"+product_name+"%';"
            data = getData(query)

            if len(data) == 1:
                product_data = data[0]['data'].split("/")
                product_label = data[0]['label'].split("/")
                n = len(product_label)
                discription = ""
                for i in range(0, n):
                    discription = discription + \
                        product_label[i] + product_data[i] + "\n"

                message_str = {
                            "attachment": {
                                "type": "template",
                                "payload": {
                                "template_type": "generic",
                                "elements": [
                                    {
                                        "title": data[0]['ten'],
                                        "image_url": data[0]['url_img'],
                                        "subtitle": discription,
                                        "default_action": {
                                        "type": "web_url",
                                        "url": data[0]['url_img'],
                                        "webview_height_ratio": "tall",
                                        },
                                        "buttons": [
                                            {
                                                "type": "postback",
                                                "title": "Đặt mua " + data[0]['ten'],
                                                "payload":"Đặt mua " + data[0]['ten']
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                }

                ret_text = "Thông tin chi tiết sản phẩm {}".format(data[0]['ten'])
                dispatcher.utter_message(text=ret_text, json_message=message_str)
            else:
                dispatcher.utter_message("có quá nhiều sản phẩm để hiển thị")
            # print(discription)
            print("chạy action_product_infor")



        return

class ActionShowListProduct(Action):
    def name(self) -> Text:
        return "action_show_list_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_company = tracker.get_slot('product_company')
        query = "select * from TGDD.DienThoai where ten like '%" +product_company+"%' limit 9;"
        phone = getData(query)
        template_items = []
        for item in phone:
            if item['gia']:
                gia = item['gia'].strip("₫")
            else:
                gia = "Chưa có thông tin về giá"
            
            template_item = {
                "title": item['ten'],
                "image_url": item['url_img'],
                "subtitle": gia,
                "default_action": {
                    "type": "web_url",
                    "url": item['url_img'],
                    "webview_height_ratio": "full"
                },
                "buttons": [
                    {
                        "type":"postback",
                        "title":"Đặt mua " + item['ten'],
                        "payload":"Đặt mua " + item['ten']
                    },
                    {
                        "type":"postback",
                        "title":"Cấu hình của {}".format(item['ten']),
                        "payload":"Cấu hình của" + item['ten'] + " như thế nào"
                    }
                ]
            }
            template_items.append(template_item)

        message_str = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": template_items

                }
            }
        }
        ret_text = "Bạn có thể chọn một trong các sản phẩm sau"
        # print(query)
        # print(phone)
        dispatcher.utter_message(text=ret_text, json_message=message_str)
        print("chạy action_show_list_product")
        return
