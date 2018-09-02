<!-- 
  <meta http-equiv="refresh" content="5;url=http://www.baidu.com"/>
-->
<table>
<?php
echo '<tr><td>PHP_SELF              </td><td>'.   $_SERVER['PHP_SELF']                ."</td></tr>"; 
echo '<tr><td>GATEWAY_INTERFACE     </td><td>'.   $_SERVER['GATEWAY_INTERFACE']       ."</td></tr>";   
echo '<tr><td>SERVER_ADDR           </td><td>'.   $_SERVER['SERVER_ADDR']             ."</td></tr>";
echo '<tr><td>SERVER_NAME           </td><td>'.   $_SERVER['SERVER_NAME']             ."</td></tr>";
echo '<tr><td>SERVER_SOFTWARE       </td><td>'.   $_SERVER['SERVER_SOFTWARE']         ."</td></tr>"; 
echo '<tr><td>SERVER_PROTOCOL       </td><td>'.   $_SERVER['SERVER_PROTOCOL']         ."</td></tr>"; 
echo '<tr><td>REQUEST_METHOD        </td><td>'.   $_SERVER['REQUEST_METHOD']          ."</td></tr>"; 
echo '<tr><td>REQUEST_TIME          </td><td>'.   $_SERVER['REQUEST_TIME']            ."</td></tr>";    
echo '<tr><td>QUERY_STRING          </td><td>'.   $_SERVER['QUERY_STRING']            ."</td></tr>";     
echo '<tr><td>HTTP_ACCEPT           </td><td>'.   $_SERVER['HTTP_ACCEPT']             ."</td></tr>";       
echo '<tr><td>HTTP_ACCEPT_CHARSET   </td><td>'.   $_SERVER['HTTP_ACCEPT_CHARSET']     ."</td></tr>";   
echo '<tr><td>HTTP_HOST             </td><td>'.   $_SERVER['HTTP_HOST']               ."</td></tr>"; 
echo '<tr><td>HTTP_REFERER          </td><td>'.   $_SERVER['HTTP_REFERER']            ."</td></tr>";     
echo '<tr><td>HTTPS                 </td><td>'.   $_SERVER['HTTPS']                   ."</td></tr>";
echo '<tr><td>REMOTE_ADDR           </td><td>'.   $_SERVER['REMOTE_ADDR']             ."</td></tr>";
echo '<tr><td>HTTP_X_FORWARDED_FOR  </td><td>'.   $_SERVER["REMOTE_ADDR"] 	      ."</td></tr>";
echo '<tr><td>HTTP_CLIENT_IP        </td><td>'.   $_SERVER["HTTP_CLIENT_IP"]          ."</td></tr>";
echo '<tr><td>REMOTE_HOST           </td><td>'.   $_SERVER['REMOTE_HOST']             ."</td></tr>";
echo '<tr><td>REMOTE_PORT           </td><td>'.   $_SERVER['REMOTE_PORT']             ."</td></tr>";
echo '<tr><td>SCRIPT_FILENAME       </td><td>'.   $_SERVER['SCRIPT_FILENAME']         ."</td></tr>";  
echo '<tr><td>SERVER_ADMIN          </td><td>'.   $_SERVER['SERVER_ADMIN']            ."</td></tr>";
echo '<tr><td>SERVER_PORT           </td><td>'.   $_SERVER['SERVER_PORT']             ."</td></tr>";
echo '<tr><td>PATH_TRANSLATED       </td><td>'.   $_SERVER['PATH_TRANSLATED']         ."</td></tr>";
echo '<tr><td>SCRIPT_NAME  	    </td><td>'.   $_SERVER['SCRIPT_NAME']             ."</td></tr>";
echo '<tr><td>SCRIPT_URI  	    </td><td>'.   $_SERVER['SCRIPT_URI']              ."</td></tr>"; 
echo '<tr><td>SERVER_SIGNATURE      </td><td>'.   $_SERVER['SERVER_SIGNATURE']        ."</td></tr>";
?>
</table>
