import java.util.concurrent.Semaphore;
import java.util.Random;
import java.util.Vector;

public class Philosopher extends Thread
{
    private static final Random rand = new Random();
    private static int event=0;
    private static String binary="";
    private int id;
    private Semaphore sem;
    private static Vector<Object[]> vector = new Vector<Object[]>();

    public Philosopher(int i, Semaphore s)
    {
        id = i;
        sem = s;
        binary = binary + "0";
    }

    private void busy()
    {
        try
        {
            sleep(rand.nextInt(1000));
        } catch (InterruptedException e){}
    }

    private void thinking()
    {
        String str = "Philosopher " + id + " is thinking";
        vector.add( this.addToObject(System.currentTimeMillis(), event , str) );
        event++;
        busy();
    }

    private void eating()
    {
        String str ="Philosopher " + id + " is hungry and is trying to pick up his chopsticks";
        vector.add( this.addToObject(System.currentTimeMillis(), event , str) );
        event++;
        busy();
        str = "Philosopher " + id + " is eating";
        this.oneToBinary(id);
        vector.add( this.addToObject(System.currentTimeMillis(), event , str) );
        event++;
        busy();
        str = "Philosopher " + id + " finished eating, and puts away his chopsticks";
        this.zeroToBinary(id);
        vector.add( this.addToObject(System.currentTimeMillis(), event , str) );
        event++;
    }

    private Object[] addToObject(long t, int i,String s ){
        Object[] o = new Object[4];
        o[3] = s;
        o[2] = i;
        o[1] = binary;
        o[0] = t;
        return o;
    }

    private void oneToBinary(int i){
        binary = binary.substring(0,i) + "1" + binary.substring(i+1);
    }

    private void zeroToBinary(int i){
        binary = binary.substring(0,i) + "0" + binary.substring(i+1);
    }

    @Override
    public void run()
    {
        for (int i = 0; i < 10; ++i)
        {
            thinking();
            try
            {
                sem.acquire();
            } catch (InterruptedException e){}
            eating();
            sem.release();
        }
    }

    public static void main(String[] args)
    {
        final int N = 5;
        Semaphore sem = new Semaphore(N, true);
        Philosopher[] philosopher = new Philosopher[N];

        // 哲学者を生成
        for (int i = 0; i < N; i++) {
          philosopher[i] = new Philosopher(i, sem);
          philosopher[i].start();
        }
        // 完了を待ち合わせる
        for (int i = 0; i < N; i++) {
          try {
            philosopher[i].join();
          } catch(InterruptedException ex) {
            return;
          }
        }

        for (int i = 0; i < vector.size(); i++) {
            Object[] o = vector.get(i);
            System.out.printf("%d %d %s %s\n", o[0], o[2], o[1], o[3]);
        }
    }
}