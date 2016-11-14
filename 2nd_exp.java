import java.util.concurrent.ThreadLocalRandom;

class Test {
   public static void main() {
      int size = 25;
      Integer[][] intList = generateIntList(size);
      Sort<Integer> sort = new Sort<Integer>();
      Integer[][][] cases = new Integer[3][4][size];
      for (int i = 0; i < 3; i++) {
         for (int j = 1; j <= 4; j++) {
            cases[i][j] = sort.sort(intList[i], j);
         }
      }
      System.out.print(intList);
      System.out.print(cases);
   }

   public static Integer[][] generateIntList(int size) {
      Integer[][] lists = new Integer[3][size];
      for (int i = 0; i < 3; i++) {
         for (int j = 0; j < size; j++) {
            switch (i) {
               case 0:
                  lists[i][j] = j;
                  break;
               case 1:
                  lists[i][j] = ThreadLocalRandom.current().nextInt(0, size * 4);
                  break;
               case 2:
                  lists[i][j] = size - j;
                  break;
               default:
                  lists[i][j] = j;
                  break;
            }
         }
      }
      return lists;
   }
}

class Sort <T extends Comparable> {
   public <T extends Comparable> T[] sort(T[] arr, int flag) {
      T[] answer;
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
         for (int j = 0; j < arr.length - i; i++) {
            if (arr[j] > arr[j + 1]) {
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
            while (inner > h - 1 && arr[inner - h] >= temp) {
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
         left = Arrays.copyOfRange(arr, 0, mid);
         right = Arrays.copyOfRange(arr, mid, arr.length);

         left = mergeSort(left);
         right = mergeSort(right);
         int i, j, k = 0;
         while (i < left.length && j < right.length) {
            if (left[i] < right[j]) {
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
         arr = moveDown(arr, i , len);
      }

      for (int i = leastParent; i > 0; i--) {
         if (arr[0] > arr[i]) {
            T temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            arr = moveDown(arr, 0, i - 1);
         }
      }
      return arr;
   }

   protected <T extends Comparable> T[] moveDown(T[] arr, int first, int last) {
      largest = 2 * first + 1;
      while (largest <= last) {
         if (largest < last && arr[largest] < arr[largest + 1]) {
            largest++;
         }
         if (arr[largest] > arr[first]) {
            T temp = arr[largest];
            arr[largest] = arr[first];
            arr[first] = temp;
            largest = 2 * first + 1;
         } else {
            return arr;
         }

      }
      return arr;
   }
}
