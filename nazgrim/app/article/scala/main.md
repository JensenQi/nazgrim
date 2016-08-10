<h1 align="center">scala代码highlight测试</h1>
<pre style="margin: 2% 5% 2% 5%;"><code class="scala">
object ScalaMain {
    def main (args: Array[String]) {
        var arr = Nd4j.create(4)
        var arr2 = Nd4j.ones(4)
        val arr3 = Nd4j.linspace(1, 10, 10)
        val arr4 = Nd4j.linspace(1, 6, 6).reshape(2, 3)
        arr += arr2
        arr += 2
        arr2 *= 5
        val arrT = arr.T
        
        println(Nd4j.sum(arr4, 0) + "Calculate the sum for each row")
        println(Nd4j.sum(arr4, 1) + "Calculate the sum for each column")
        println(Arrays.toString(arr2.shape) + "Checking array shape")
        println(arr2.toString() + "Array converted to string")
        println(arr2.assign(5) + "Array assigned value of 5 (equivalent to fill method in numpy)")
        println(arr2.reshape(2, 2) + "Reshaping array")
        println(arr2.ravel + "Raveling array")
        println(Nd4j.toFlattened(arr2) + "Flattening array (equivalent to flatten in numpy)")
        println(Nd4j.sort(arr2, 0, true) + "Sorting array")
        println(Nd4j.sortWithIndices(arr2, 0, true) + "Sorting array and returning sorted indices")
        println(Nd4j.cumsum(arr2) + "Cumulative sum")
        println(Nd4j.mean(arr) + "Calculate mean of array")
        println(Nd4j.std(arr2) + "Calculate standard deviation of array")
        println(Nd4j.`var`(arr2), "Calculate variance")
        println(Nd4j.max(arr3), "Find max value in array")
        println(Nd4j.min(arr3), "Find min value in array")
    
    }
}
</code></pre>