import org.junit.jupiter.api.Test;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.test.TestRabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import ru.scco.pdf_generator.Receiver;
import ru.scco.pdf_generator.dto.PDFGeneratorRequestDTO;
import ru.scco.pdf_generator.processors.ProcessingChain;


@SpringBootTest(classes = {TestConfig.class, Receiver.class, ProcessingChain.class})
public class SpeedTest {
    @Autowired
    private TestRabbitTemplate testRabbitTemplate;

    @Autowired
    private Queue inputQueue;

    @Test
    public void speedTest() {

        long start = System.nanoTime();
        for (int i = 0; i < 1000; ++i) {
            testRabbitTemplate.convertAndSend(
                    inputQueue.getName(),
                    new PDFGeneratorRequestDTO(
                            i,
                            i, "Здравствуйте, Акакий "
                               + "Акакиевич!\nМы"
                               + " увидели ваше"
                               + " сообщение в канале @overcoat. Хотим предложить "
                               + "вам свои услуги. Наша команда OwlWeb занимается "
                               + "пошивом шинелей 181 год. "
                               + "Если вас заинтересовало предложение — напишите "
                               + "ответ на сообщение или позвоните нашему "
                               + "менеджеру.\n"
                               + "Здравствуйте, Акакий "
                               + "Акакиевич!\nМы"
                               + " увидели ваше"
                               + " сообщение в канале @overcoat. Хотим предложить "
                               + "вам свои услуги. Наша команда OwlWeb занимается "
                               + "пошивом шинелей 181 год. "
                               + "Если вас заинтересовало предложение — напишите "
                               + "ответ на сообщение или позвоните нашему "
                               + "менеджеру."
                               + "\n",
                            "88005353535"));
        }
        System.out.println((System.nanoTime() - start) / 1000000);
    }
}