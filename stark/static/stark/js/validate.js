(function(jq){

	function ErrorMessage(container,msg){
		$error = container.find("label[class='input-error']");
		if($error.length>0){
			$error.text(msg);
		}else{
			var temp = "<label class='input-error'>"+msg+"</label>";
			container.append(temp);
		}

	}

	function EmptyError(container){
		$error = container.find("label[class='input-error']");
		if($error.length>0){
			$error.remove();
		}
	}

	jq.extend({
		'CheckAll':function(targetcontainer){
			$(targetcontainer).find(':checkbox').attr('checked',true);
		},
		'UnCheckAll':function(targetcontainer){
			$(targetcontainer).find(':checkbox').attr('checked',false);
		},
		'ReverseCheck':function(targetcontainer){
			$(targetcontainer).find(':checkbox').each(function(){
				var check = $(this).attr('checked');
				console.log(check);
				if(check){
					$(this).attr('checked',false);
				}else{
					$(this).attr('checked',true);
				}
			})
		},
		'Hide':function(target){
			$(target).addClass('hide');
		},
		'Show':function(target){
			$(target).removeClass('hide');
		},
		'register':function(form,summaryStatusId){
			$(form).find(':submit').click(function(){
				var flag = true;


				$(form).find(':text,:password').each(function(){
					var name = $(this).attr('name');
					var label = $(this).attr('label');
					var val = $(this).val();
					var $parent = $(this).parent();

					//<label class='input-error'>用户名长度只能在4-20位字符之间</label>
					//<label class='input-error'>用户名只能由中文、英文、数字及"-"、"_"组成</label>

					var required = $(this).attr('require');
					if(required){
						if(!val || val.trim() == ''){
							flag = false;
							ErrorMessage($parent,label+'不能为空.');
							return false;
						}
					}

					var confirm_to = $(this).attr('confirm-to');
					if(confirm_to){
						var $original = $(form).find("input[name='"+confirm_to+"']");
						if($original.val().trim()!=val.trim()){
							flag = false;
							ErrorMessage($parent,'两次密码输入不一致.');
							return false;
						}
					}

					var number = $(this).attr('number');
					if(number){
						if(!$.isNumeric(number)){
							flag = false;
							ErrorMessage($parent,label+'必须为数字.');
							return false;
						}
					}

					var mobile = $(this).attr('mobile');
					if(mobile){
						var reg = /^1[3|5|8]\d{9}$/;
						if(!reg.test(val)){
							flag = false;
							ErrorMessage($parent,label+'格式错误.');
							return false;
						}
					}

					var min = $(this).attr('min-len');
					if(min){
						var len = parseInt(min)
						if(val.length<len){
							flag = false;
							ErrorMessage($parent,label+'最小长度为'+min+'.');
							return false;
						}
					}

					var max = $(this).attr('max-len');
					if(max){
						var len = parseInt(max)
						if(val.length>len){
							flag = false;
							ErrorMessage($parent,label+'最大长度为'+max+'.');
							return false;
						}
					}

					var range = $(this).attr('range');
					if(range){
						var len = range.split('-');
						if(val.length<parseInt(len[0])||val.length>parseInt(len[1])){
							flag = false;
							ErrorMessage($parent,label+'长度只能在'+len[0]+'-'+len[1]+'位字符之间.');
							return false;
						}
					}

					var field = $(this).attr('Field');
					if(field=='string'){
						var reg = /^\w+$/;
						if(!reg.test(val)){
							flag = false;
							ErrorMessage($parent,label+'只能由英文、数字及"_"组成.');
							return false;
						}
					}
					EmptyError($parent);
				});


                var check = $("#protocol").prop('checked');

                if(!check){
                    flag = false;
                    try{
                        ErrorMessage($("#protocol").parent().parent(),'请阅读用户注册协议.');
                    }catch(e){
                        flag = false;
                    }
                }else{
                    EmptyError($("#protocol").parent().parent());
                }

				return flag;
			});
		},
		'login':function(form,summaryStatusId){
			$(form).find(':submit').click(function(){
				var flag = true;


				$(form).find(':text,:password').each(function(){
					var name = $(this).attr('name');
					var label = $(this).attr('label');
					var val = $(this).val();
					var $parent = $(this).parent();

					var required = $(this).attr('require');
					if(required){
						if(!val || val.trim() == ''){
							flag = false;
							ErrorMessage($parent,label+'不能为空.');
							return false;
						}
					}

					EmptyError($parent);
				});

				return flag;
			});
		},
	});


})(jQuery)