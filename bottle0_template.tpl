<table>
<tr style="background-color:#CCCFDF"><th colspan="2">API
Documentation</th></tr>
<tr style="background-color:#CCCFDF"><th>ENDPOINT</th><th>DESC</th></tr>
 % for color,resource in zip(colors,routes) :
   % docx = resource.callback.__doc__
   <tr style="background-color:{{ color }}"><td>{{ resource.rule }}</td><td>
{{! docx.replace("\n","<br/>") if docx else "Not documented" }} </td></tr>
 % end
 </table>
