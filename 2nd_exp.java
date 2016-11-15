import java.util.concurrent.ThreadLocalRandom;
import java.lang.Comparable;
import java.util.Arrays;

class Test {
   public static final String[] type = {"Sorted", "Random", "Reversed"};

   public static void main(String[] args) {
      int size = 52;
      Integer[][] intList = generateIntList(size);
      Sort<Integer> sort = new Sort<Integer>();
      Integer[][][] cases = new Integer[3][4][size];
      long[][] times = new long[3][4];
      for (int i = 0; i < 3; i++) {
         for (int j = 1; j <= 4; j++) {
            long startTime = System.nanoTime();
            cases[i][j - 1] = sort.sort(Arrays.copyOf(intList[i], intList[i].length), j);
            long endTime = System.nanoTime();
            times[i][j - 1] = endTime - startTime;
         }
      }

      for (int i = 0; i < 4; i++) {
         System.out.println(Sort.NAMES[i]);
         for (int j = 0; j < 3; j++) {
            System.out.println(type[j] + ": " + times[j][i] / 1000.0 + " microseconds");
         }
         System.out.println();
      }

   }

   public static Integer[][] generateIntList(int size) {
      Integer[][] lists = new Integer[3][size];
      for (int i = 0; i < 3; i++) {
         for (int j = 0; j < size; j++) {
            switch (i) {
               case 0: //Sorted
                  lists[i][j] = j;
                  break;
               case 1: //Random
                  lists[i][j] = ThreadLocalRandom.current().nextInt(0, size * 4);
                  break;
               case 2: //Reversed
                  lists[i][j] = size - j;
                  break;
            }
         }
      }
      return lists;
   }
}

class Sort <T extends Comparable> {
   public static final String[] NAMES = {"Bubble Sort", "Shell Sort", "Merge Sort", "Heap Sort"};

   public <T extends Comparable> T[] sort(T[] arr, int flag) {
      T[] answer = null;
      switch (flag) {
         case 1:
            answer = bubbleSort(arr);
            break;
         case 2:
            answer = shellSort(arr);
            break;
         case 3:
            answer = mergeSort(arr);
            break;
         case 4:
            answer = heapSort(arr);
            break;
         default:
            break;
      }
      return answer;
   }


   protected <T extends Comparable> T[] bubbleSort(T[] arr) {
      for (int i = 0; i < arr.length; i++) {
         for (int j = 0; j < (arr.length - i - 1); j++) {
            if (arr[j].compareTo(arr[j + 1]) > 0) {
               T temp = arr[j];
               arr[j] = arr[j + 1];
               arr[j + 1] = temp;
            }
         }
      }
      return arr;
   }

   /*********************************************************************
    * Help received from
    * http://stackoverflow.com/questions/4833423/shell-sort-java-example
    *********************************************************************/
   protected <T extends Comparable> T[] shellSort(T[] arr) {
      int inner, outer;
      T temp;
      //find initial value of h
      int h = 1;
      while (h <= arr.length / 3)
         h = h * 3 + 1; // (1, 4, 13, 40, 121, ...)

      while (h > 0) // decreasing h, until h=1
      {
         // h-sort the file
         for (outer = h; outer < arr.length; outer++) {
            temp = arr[outer];
            inner = outer;
            // one subpass (eg 0, 4, 8)
            while (inner > h - 1 && temp.compareTo(arr[inner - h]) < 0) {
               arr[inner] = arr[inner - h];
               inner -= h;
            }
            arr[inner] = temp;
         }
         h = (h - 1) / 3; // decrease h
      }
      return arr;
   }

   protected <T extends Comparable> T[] mergeSort(T[] arr) {
      if (arr.length > 1) {
         int mid = arr.length / 2;
         T[] left = Arrays.copyOfRange(arr, 0, mid);
         T[] right = Arrays.copyOfRange(arr, mid, arr.length);

         left = mergeSort(left);
         right = mergeSort(right);
         int i, j, k;
         i = j = k = 0;
         while (i < left.length && j < right.length) {
            if (left[i].compareTo(right[j]) < 0) {
               arr[k] = left[i];
               i++;
            } else {
               arr[k] = right[j];
               j++;
            }
            k++;
         }
         while (i < left.length) {
            arr[k] = left[i];
            i++;
            k++;
         }
         while (j < right.length) {
            arr[k] = right[j];
            j++;
            k++;
         }
      }
      return arr;
   }

   protected <T extends Comparable> T[] heapSort(T[] arr) {
      int len = arr.length - 1;
      int leastParent = len / 2;
      for (int i = leastParent; i >= 0; i--) {
         arr = moveDown(arr, i, len);
      }

      int N = len;
      for (int i = len; i > 0; i--) {
         T temp = arr[0];
         arr[0] = arr[i];
         arr[i] = temp;
         N--;
         arr = moveDown(arr, 0, N);
      }
      return arr;
   }

   protected <T extends Comparable> T[] moveDown(T[] arr, int i, int N) {
      int left = 2 * i;
      int right = 2 * i + 1;
      int max = i;
      if (left <= N && arr[left].compareTo(arr[i]) > 0) {
         max = left;
      }
      if (right <= N && arr[right].compareTo(arr[max]) > 0) {
         max = right;
      }

      if (max != i) {
         T temp = arr[i];
         arr[i] = arr[max];
         arr[max] = temp;
         arr = moveDown(arr, max, N);
      }
      return arr;
   }
}
