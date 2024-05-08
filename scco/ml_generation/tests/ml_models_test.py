# import ml_models.gigachat_api_gate.api as ml_models_api
import ml_models.co_gen.api as co_gen_api
import ml_models.white_list_generation.api as whitelist_gen_api

# TODO: expected API as below

co_gen = co_gen_api.SCCOGenerator()

request = {
    "customer_id": "customer_1",
    "contact_info": "<@telegram_link>",
    "company_name": "Web сфера",
    'channel_ids': "Outstaffing",
    'messages': ["вакансия #работа #job #ios #swift вакансия ios-разработчик. компания лайв тайпинг. город удалённо. формат работы удаленно. уровень зп от 200 000 до 300 000 в месяц. опыт в разработке ios от 3-х лет. тип занятости full-time вариант оформления самозанятость или ип. гражданство и локация кандидата рф привет мы компания лайв тайпинг уже более 13 лет создаём мобильные приложения и веб-сервисы мы сотрудничали с такими известными брендами как sephora иль дэ ботэ pepsico samsung mastercard httplivetypingcomruмы ищем ios-разработчика который хочет работать с нами в формате аутстафф стек на котором мы работаем. viper-c. rxswift. rswift. moya. resolverdi. swiftlint swiftformat. snapkit. codable. fakery для моков ты нам подходишь если имеешь опыт разработки приложений не менее 3-х лет уверенно владеешь rxswift пишешь качественный и чистый код преимущества работы с нами гибкий график и работа на удалёнке мы берем на себя все заботы по поиску проекта общения с заказчиком и оплате помогаем договориться с клиентом о графике дейликов и работы удобном для тебя возможность совмещать с другими проектами возможность взять следующий проект если нам понравится сотрудничать друг с другом буду рада обсудить детали. кристина. тг @christinait"],
    "black_list": [
        "php",
        "wordpress",
        "c#",
    ],
    "tags": [
        "frontend",

        "android",
        "ios",

        "react",
        "nodejs",

        "javascript",
        "vue",

        "typescript",

        "figma",
        "flutter",
        "photoshop",
        "web",

        "css",
        "css3",
        "html",
        "html5",

        "REST",
        "вёрстка",
        "веб-сайт"
    ],
    "white_list": [
        "frontend",

        "android",
        "ios",

        "react",
        "nodejs",

        "javascript",
        "vue",

        "typescript",

        "figma",
        "flutter",
        "photoshop",
        "web",

        "css",
        "css3",
        "html",
        "html5",

        "REST",
        "вёрстка",
        "веб-сайт"
    ],
    "specific_features": [
        "Мы - российская компания по разработке программного обеспечения, ориентированная на технологические процессы.",
        "Мы помогаем другим компаниям взаимодействовать со своей аудиторией с помощью высококачественных веб-приложений и мобильных устройств на платформе android.",
        "У нас имеется 25-летний опыт веб-разработки и веб-хостинга",
        "Мы рассматриваем наших клиентов как стратегических деловых партнеров. Поэтому выбор нас для создания вашего веб-сайта - это только первый этап в долгосрочных деловых отношениях.",
        "У нас сотни клиентов по всему миру. Некоторые из них работают у нас более 15 лет, что является беспрецедентным в этой отрасли."
    ],
    "customer_services": [
        {
            "customer_id": "customer_1",
            "service_name": "Создание MVP",
            "service_desc": "Запускаете новый продукт? Наши услуги по разработке MVP основаны на быстром прототипировании и гибкой методологии, позволяющей быстро и эффективно выводить ваши идеи на рынок."
        },
        {
            "customer_id": "customer_1",
            "service_name": "UX/UI дизайн",
            "service_desc": "Наши услуги по дизайну продуктов позволяют по-новому взглянуть на разработку программного обеспечения, которую возглавляют эксперты в области консалтинга по дизайну продуктов. Мы не просто консультанты по дизайну продуктов; мы новаторы в разработке дизайна, ориентированного на пользователя."
        },
        {
            "customer_id": "customer_1",
            "service_name": "Модернизация устаревшего UI",
            "service_desc": "Преобразуем ваш пользовательский интерфейс в соответствии с современными стандартами. Наши услуги по модернизации пользовательского интерфейса делают ваши приложения более привлекательными и удобными для пользователя."
        },
    ]
}


main_response = co_gen.generate(request)
print(main_response["main_text"])

import json
for num in range(3, 15+1):
    with open('clients_messages/'+f'clients_messages_{num}.txt', 'r', encoding='utf-8') as f:
       d = json.load(f)
       request['messages'] = d['messages']
    main_response = co_gen.generate(request)
    with open(f'answers/ans{num}.txt', 'w') as f:
        f.write(main_response['main_text'])
