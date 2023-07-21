import java.util.*;
class somefile {

    private static void privatefunct(int ind, int target, List<Integer> ds, int[] candidates, List<List<Integer>> ans)
    {
        if (target == 0)
        {
            ans.add(new ArrayList<Integer>(ds));
            return;
        }
        for (int i=ind; i < candidates.length; i++)
        {
            if ((i > ind) && (candidates[i]) == candidates[i - 1])
            {
                continue;
            }
            if (candidates[i] > target)
            {
                break;
            }

            ds.add(candidates[i]);
            privatefunct(i + 1, target - candidates[i], ds, candidates, ans);
            ds.remove(ds.size() - 1);
        }
    }
    public static List<List<Integer>> combinationSum2(int[] candidates, int target) {
        List<List<Integer>> ans = new ArrayList<List<Integer>>();
        List<Integer> ds = new ArrayList<Integer>();
        Arrays.sort(candidates);
        privatefunct(0, target, ds, candidates, ans);
        return ans;
        
    }

    public static void main(String[] args) {
        int[] lis = {1, 2, 3, 4, 5, 6, 7, 8};
        int tar = 6;
        List<List<Integer>> ans = combinationSum2(lis, tar);

        for(List<Integer> l : ans)
        {
            System.out.print("  [");
  
            for (int item : l) {
                System.out.print("  "
                                 + item
                                 + ", ");
            }
            System.out.println("], ");
        }
        }
    }