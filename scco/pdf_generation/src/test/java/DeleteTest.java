import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import ru.scco.pdf_generator.InvalidCPException;
import ru.scco.pdf_generator.processors.ProcessingChain;


public class DeleteTest {
    ProcessingChain chain = new ProcessingChain();

    @Test
    public void nothingToDeleteTest() throws InvalidCPException {
        String cp = "Все говорят: Кремль, Кремль. Ото всех я слышал про него,"
                    + " а сам ни разу не видел. Сколько раз уже (тысячу раз),"
                    + " напившись, или с похмелюги, проходил по Москве с севера на юг, с запада на восток, из конца в конец и как попало — и ни разу не видел Кремля.";
        Assertions.assertEquals(cp, chain.process(cp));
    }

    @Test
    public void oneSentenceToDelete() throws InvalidCPException {
        String cp = "- И немедленно выпил… - Нет, вот уж теперь — жить и "
                    + "жить! А жить совсем не скучно! Скучно было жить только"
                    + " Николаю Гоголю и царю Соломону. Если уж мы прожили тридцать лет, надо попробовать прожить еще тридцать, да, да. «Человек смертен» — таково мое мнение. Но уж если мы родились, ничего не поделаешь — надо немножко пожить… «Жизнь прекрасна» — таково мое мнение.";
        String partToDelete = "С уважением, Панки";
        Assertions.assertEquals(cp, chain.process(cp + partToDelete));
    }

    @Test
    public void twoSentenceToDelete() throws InvalidCPException {
        String cp =
                "- И немедленно выпил… - И немедленно выпил… - Нет, вот уж теперь — жить и "
                + "жить! А жить совсем не скучно! Скучно было жить только"
                + " Николаю Гоголю и царю Соломону. Если уж мы прожили тридцать лет, надо попробовать прожить еще тридцать, да, да. «Человек смертен» — таково мое мнение. Но уж если мы родились, ничего не поделаешь — надо немножко пожить… «Жизнь прекрасна» — таково мое мнение.";
        String partToDelete = "С уважением, Панки.";
        System.out.println(chain.process(cp + partToDelete + partToDelete));
        Assertions.assertEquals(cp, chain.process(
                cp + partToDelete + partToDelete));
    }

    @Test
    public void tooSmallCPTest() {
        Assertions.assertThrows(InvalidCPException.class, () -> chain.process(
                "- И немедленно выпил…"));
    }

    @Test
    public void bracketsTest() throws InvalidCPException {
        Assertions.assertEquals("Доброе утро, клиент_1!\n"
                                + "Мы рады приветствовать вас в нашей компании \"Company of customer 1\". Наша\n"
                                + "компания специализируется на предоставлении услуг в области разработки\n"
                                + "программного обеспечения. Мы обладаем большим опытом в разработке\n"
                                + "программного обеспечения на языке программирования Python.\n"
                                + "Мы предлагаем вам услуги высококвалифицированных разработчиков Python,\n"
                                + "которые обладают глубокими знаниями и опытом в области разработки\n"
                                + "программного обеспечения. Наши разработчики способны решать сложные\n"
                                + "задачи и создавать инновационные решения, которые помогут вам достичь\n"
                                + "ваших бизнес-целей.\n"
                                + "Мы также предлагаем услуги по обучению и развитию навыков Python. Если у вас\n"
                                + "есть команда разработчиков, мы можем провести тренинги и семинары, чтобы\n"
                                + "повысить их навыки и знания в области Python.\n"
                                + "Наша компания также предоставляет услуги по тестированию и отладке\n"
                                + "программного обеспечения на языке Python. Мы гарантируем высокое качество и\n"
                                + "надежность наших услуг.\n"
                                + "Если у вас есть какие-либо вопросы или потребности в услугах Python\n"
                                + "разработчиков, пожалуйста, свяжитесь с нами. Мы будем рады помочь вам и\n"
                                + "предложить наилучшие решения для вашего "
                                + "бизнеса.\n", chain.process("Доброе утро, "
                                                            + "клиент_1!\n"
                                         + "Мы рады приветствовать вас в нашей компании \"Company of customer 1\". Наша\n"
                                         + "компания специализируется на предоставлении услуг в области разработки\n"
                                         + "программного обеспечения. Мы обладаем большим опытом в разработке\n"
                                         + "программного обеспечения на языке программирования Python.\n"
                                         + "Мы предлагаем вам услуги высококвалифицированных разработчиков Python,\n"
                                         + "которые обладают глубокими знаниями и опытом в области разработки\n"
                                         + "программного обеспечения. Наши разработчики способны решать сложные\n"
                                         + "задачи и создавать инновационные решения, которые помогут вам достичь\n"
                                         + "ваших бизнес-целей.\n"
                                         + "Мы также предлагаем услуги по обучению и развитию навыков Python. Если у вас\n"
                                         + "есть команда разработчиков, мы можем провести тренинги и семинары, чтобы\n"
                                         + "повысить их навыки и знания в области Python.\n"
                                         + "Наша компания также предоставляет услуги по тестированию и отладке\n"
                                         + "программного обеспечения на языке Python. Мы гарантируем высокое качество и\n"
                                         + "надежность наших услуг.\n"
                                         + "Если у вас есть какие-либо вопросы или потребности в услугах Python\n"
                                         + "разработчиков, пожалуйста, свяжитесь с нами. Мы будем рады помочь вам и\n"
                                         + "предложить наилучшие решения для вашего бизнеса.\n"
                                         + "[Your Company Name]"));

        Assertions.assertEquals("Здравствуйте! Мы рады предложить вам услуги наших опытных разработчиков,\n"
                                + "специализирующихся на PHP. У нас есть команда профессионалов, которые\n"
                                + "готовы взяться за ваш проект и обеспечить его успешное выполнение.\n"
                                + "Наш основной проект написан на PHP, и мы готовы доработать его в\n"
                                + "соответствии с вашими требованиями. Мы также можем помочь вам с\n"
                                + "реализацией реалтайм части приложения, используя Node.js, Express и Socket.io.\n"
                                + "Мы работаем в офисе в Москве, но также готовы рассмотреть удаленную работу,\n"
                                + "если это будет удобно для вас.\n"
                                + "Если вы заинтересованы в наших услугах, пожалуйста, свяжитесь с нами для\n"
                                + "обсуждения деталей проекта. Мы готовы предоставить вам подробную\n"
                                + "информацию о наших возможностях и опыте "
                                + "работы.", chain.process("Здравствуйте! Мы рады предложить вам услуги наших опытных разработчиков,\n"
                                                                 + "специализирующихся на PHP. У нас есть команда профессионалов, которые\n"
                                                                 + "готовы взяться за ваш проект и обеспечить его успешное выполнение.\n"
                                                                 + "Наш основной проект написан на PHP, и мы готовы доработать его в\n"
                                                                 + "соответствии с вашими требованиями. Мы также можем помочь вам с\n"
                                                                 + "реализацией реалтайм части приложения, используя Node.js, Express и Socket.io.\n"
                                                                 + "Мы работаем в офисе в Москве, но также готовы рассмотреть удаленную работу,\n"
                                                                 + "если это будет удобно для вас.\n"
                                                                 + "Если вы заинтересованы в наших услугах, пожалуйста, свяжитесь с нами для\n"
                                                                 + "обсуждения деталей проекта. Мы готовы предоставить вам подробную\n"
                                                                 + "информацию о наших возможностях и опыте работы.[Ваше имя]\n"
                                                                 + "[Ваша должность]\n"
                                                                 + "[Ваша компания]"));
    }
}
