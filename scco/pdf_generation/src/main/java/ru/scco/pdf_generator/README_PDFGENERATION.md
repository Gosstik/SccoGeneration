# PDFGENERATION

Причины текущей реализации:

1. Используется генерация из шаблона, так как наверняка захочется его персонализировать
2. Можно было в качестве шаблона брать не pdf, а xml/docs и прочее. Такие шаблоны было бы удобнее заполнять программно, но:
   1. Если в дальнейшем шаблоны будет предоставлять пользователь - ему удобнее pdf
   2. Конвертация из других форматов в pdf может быть непредсказуемой. Редко, но бывает, что склеиваются поля
3. Чтобы при этом можно было задавать в шаблоне местоположение текста, используется текстовая форма. Форма содержит информацию о месте текста, его размере, цвете и шрифте. Программно получить доступ к ней можно по ее имени
4. Не все приложения по созданию pdf работают с русским шрифтами в форме. Чтобы гарантированно не было проблем, при заполнении используется заданный программой, а не шаблоном шрифт. Размер и цвет используются как в шаблоне
5. В pdfbox функционал PDTextField, который соответствует форме ограничен. В частности нельзя обработать переполнение формы. Поэтому запись ведется в contentStream, созднанный по параметрам формы



PDFGenerator:

Основной метод fillMultiPageTemplate - создает документ, находит форму main_text и на ее основе создает contentStream. Вызывыает showLongLine для каждой строки. Если случилось переполнение поля, создает новую страницу с contentStream на ней. В конце сохраняет в файл.

Метод showLongLine - пишет в contentStream, разбивая слишком длинные строки. При переполнении поля возвращает невместившийся текст.

Переполнение отслеживается через  PDRectangle rectangle, принимаемый как 1 из параметров  showLongLine. При переносе строки верхняя граница rectangle сдвигается.&#x20;

```
У ContentStream нет автоматического wrapping
Можно было бы вместо записи в ContentStream писать в сам PDTextField.
Там есть автоматический wrapping, однако там нельзя обработать 
переполнение поля.

Для текущей задачи не актуально, но может понадобиться в будещем: 
в contentStream есть возможноть динамической смены font
(т.е. часть текста писать одним font, часть другим. То же относится
к размеру и цвету текста)
В PDTextField такой возможности нет.
```

#### Объяснение showLongLine:

Символы имеют различную ширину, поэтому необходимо проверять размер каждого. Wrapping осуществляется по пробельным символам, если это возмжно. Иначе - по последнему не выходящему за границы символы.&#x20;

В wordBuilder хранится последнее считанное слово, в lineBuilder - текст до него,  не записанный в contentStream. При достижении ширины поля, в contentStream пишется текст до последнего считанного слова (т.е. весь lineBuilder). Если же lineBuilder был пуст (т.е. нет возможности разделить по пробелам), пишется wordBuilder. Если очередной считанный символ был пробельным, wordBuilder добавляется в lineBuilder

#### Краткий гайд по pdfbox и объяснение fillMainTemplate:

PDType0Font - тип font, поддерживающий не ascii

PDAcroForm - хранилище форм. Через метод getField можно по имени получить требуемую форму

У формы может быть несколько виджетов с разным местоположением. (Если формы в pdf-документе назвать одинаково, то это одна форма с несколькими виджетами. При заполнении такой формы заполняются все ее виджеты одним и тем же текстом). В шаблоне, используемом программой виджет только 1. В виджете задаются данные о местоположении текста (координты виджета, его размер).&#x20;

PDRectangle - информация о координатах виджета.

Чтобы можно было скопировать офромление страницы, в том числе все помимо формы main\_text, нужно из страницы создать форму и добавлять эту форму как layer. Этим занимается LayerUtility







