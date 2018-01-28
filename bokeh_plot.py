# TO DO:
# 1.) add area under curve
# 2.) add updated heads and tails
# 3.) add stats
# 4.) move JS to file
# 5.) add comments!
# 6) clean imports

import numpy as np
import random

from bokeh.embed import components
from bokeh.layouts import column
from bokeh.plotting import Figure, show
from bokeh.models import ColumnDataSource, CustomJS, Patch
from bokeh.models.widgets import Button, DataTable, PreText, TableColumn


def create_plot(Pi=0.5):
    n = 1000
    x = np.linspace(0, 1, n)
    p = np.ones(n)

    a = 1
    b = 1

    s1 = ColumnDataSource(data=dict(x=x, p=p))
    s2 = ColumnDataSource(data=dict(params=[Pi, a, b]))

    plot = Figure()
    plot.xaxis.axis_label = 'Probability of Heads (-)'
    plot.yaxis.axis_label = 'Probability Density (-)'

    plot.line('x', 'p', source=s1, line_width=4)

    # patch = Patch(x='x', y='p', fill_color='#a6cee3')
    # plot.add_glyph(s1, patch)

    callback = CustomJS(args=dict(s1=s1, s2=s2), code="""

        // gamma function
        function gamma(n) {
          n -= 1;
          if (n == 0 || n == 1)
            return 1;
          for (var i = n - 1; i >= 1; i--) {
            n *= i;
          }
          return n;
        }

        // beta function
        function beta(a, b) {
          return gamma(a)*gamma(b)/gamma(a + b)
       }

        // flip coin function
        function flip_coin(Pi, a, b) {
          prob = Math.random();
          if (prob < Pi) {
            return [a + 1, b];
          }
          return [a, b + 1];
        }

        // get data sources from Callback args
        var d1 = s1.data;
        var d2 = s2.data;

        // unpack variables from data sources
        var x = d1['x'];
        var p = d1['p'];
        var params = d2['params'];

        // update shape parameters
        var Pi = params[0]
        var a = params[1];
        var b = params[2];

        var updated_params = flip_coin(params[0], params[1], params[2]);
        params[1] = updated_params[0];
        params[2] = updated_params[1];
        var a = params[1];
        var b = params[2];

        // update probability
        for (i = 0; i < x.length; i++) {
          p[i] = Math.pow(x[i], a - 1)*Math.pow(1 - x[i], b - 1)/beta(a, b)
        }

        // emit update to data sources
        s1.change.emit();
        s2.change.emit();
    """)

    button = Button(label='Flip Coin', callback=callback)
    layout = column(button, plot)

    return components(layout)


if __name__ == '__main__':
    script, div = create_plot()
