import java.util.concurrent.*;
import java.util.*;

class Task {
    private int id;

    public Task(int id) {
        this.id = id;
    }

    public int process() throws InterruptedException {
        Thread.sleep(500); // simulate work
        return id * 2;
    }
}

class Worker implements Runnable {
    private BlockingQueue<Task> queue;
    private List<Integer> results;

    public Worker(BlockingQueue<Task> queue, List<Integer> results) {
        this.queue = queue;
        this.results = results;
    }

    @Override
    public void run() {
        while (true) {
            try {
                Task task = queue.poll(2, TimeUnit.SECONDS);
                if (task == null) break;

                System.out.println(Thread.currentThread().getName() + " processing task");
                int result = task.process();

                synchronized (results) {
                    results.add(result);
                }

            } catch (InterruptedException e) {
                System.out.println("Thread interrupted: " + e.getMessage());
                break;
            }
        }
    }
}

public class Main {
    public static void main(String[] args) {
        BlockingQueue<Task> queue = new LinkedBlockingQueue<>();
        List<Integer> results = Collections.synchronizedList(new ArrayList<>());

        for (int i = 1; i <= 10; i++) {
            queue.add(new Task(i));
        }

        ExecutorService executor = Executors.newFixedThreadPool(3);

        for (int i = 0; i < 3; i++) {
            executor.execute(new Worker(queue, results));
        }

        executor.shutdown();

        try {
            executor.awaitTermination(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            System.out.println("Execution interrupted");
        }

        System.out.println("Results: " + results);
    }
}