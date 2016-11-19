<h1 align="center">java代码highlight测试</h1>
<pre style="margin: 2% 5% 2% 5%;"><code class="java">
import java.text.SimpleDateFormat;
import java.util.Date;
//将long字符串转换成格式时间输出
public class LongToString {
    public static void main(String argsp[]){
	    String time = "1256006105375";
	    Date date = new Date(Long.parseLong(time));
	    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
	    time = formatter.format(date);
	    System.out.println(time);
    }
}

</code></pre>