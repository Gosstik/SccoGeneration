request_simple = {
    "request_name": "get_info_for_co_generation",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_routing_key",
    },
    "reply_ctx": 1,  # not required
    "request_data": {
        "message_group_id": 1,
    }
}

################################################################################

answer_simple = {
  "customer_id": "customer_1",
  "client_id": "client_1",
  "channel_ids": [
    "phystech.career"
  ],
  "messages": [
    "#ищу\nНужен разработчик на python для вёрстки сайта авто компании.\nПредложения пишите в телеграм: @client_1_tg"
  ],
  "attitude": "Вы",
  "company_name": "Web Сфера",
  "tags": [
    "frontend",
    "вёрстка"
  ],
  "white_list": [
    "frontend",
    "вёрстка",
    "javascript",
    "веб-сайт"
  ],
  "specific_features": [
    "25-летний опыт.",
    "Cотни довольных клиентов."
  ],
  "customer_services": [
    {
      "service_name": "Создание MVP",
      "service_desc": "Запуск нового продукта."
    },
    {
      "service_name": "Модернизация UI",
      "service_desc": "Преобразуем устаревший UI."
    },
    {
      "service_name": "Электрика",
      "service_desc": "Монтаж кабель-канала."
    },
    {
      "service_name": "Сантехника",
      "service_desc": "Установка смесителей."
    }
  ],
  "reply_ctx": 1
}
