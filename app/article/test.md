When $ a \ne 0 $, there are two solutions to $ ax^2 + bx + c = 0 $ and they are:
$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$

\begin{equation}
\begin{aligned}
\dot{x} & = \sigma(y-x) \newline
\dot{y} & = \rho x - y - xz \newline
\dot{z} & = -\beta z + xy
\end{aligned}
\end{equation}
Here is a labeled equation:
$$x+1\over\sqrt{1-x^2}\label{ref1}$$
with a reference to ref1: \eqref{ref1},

#python代码highlight测试
<pre style="margin: 2% 5% 2% 5%;"><code class="python">
# -*- coding:utf-8 -*-
__author__ = 'jinxiu.qi'
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __table__name = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password 只有写权限')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'user', self.id, self.name
</code></pre>

#java代码highlight测试
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
