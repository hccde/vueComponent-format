<style type="text">
	    .popup {
        width: rem(600);
        height: rem(600);
        background-color:white;
        overflow: auto;
        .question {
            padding-left:rem(30);
            display: flex;
            align-items:center;
            min-height: rem(100);
            font-size: rem(32);
            padding-top:rem(34);
            padding-bottom:rem(34);
            .answer {
            }
        }
    }
    ul {
        width: 100%
            height: auto;
        padding-left:rem(30);
        padding-right:rem(30);
        font-size:rem(32);
        li {
            border-top: 1px solid #e5e5e5;
            width: 100%;
            min-height: rem(100);
            font-size: rem(32);
            display: flex;
            align-items:center;
            justify-content: space-between;
        }
    }
    

  	
</style> 
<template>
    <div class = "activity-detail">
        <ul class = "flexbox-parent detail-section statistics">
            <li class = "flexbox-child">
                报名
                <br>
                {{ signedCount }}
            </li>
            <li class = "flexbox-child">
                阅读
                <br>
                {{ readedCount }}
            </li>
        <!-- <li class="flexbox-child">分享<br>{{ sharedcount }}</li> -->
            <li class = "flexbox-child">
                评论
                <br>
                {{ commentCount }}
            </li>
        </ul>
        <div class = "detail-section">
            <mt-cell v-for = "menu in menus" :title = "menu.title" is-link @click.native = "linkto(menu)"></mt-cell>
        </div>
        <mt-cell class = "detail-section" title = "开启报名">
            <mt-switch :value = "signenabled" @change.native = "updatestatus(signenabled)"></mt-switch>
        </mt-cell>
        <interaction-block :component-list = "sharelist"></interaction-block>
    </div>
</template>



<script type="text/javascript">
import {
    string2Array
} from '../../helpers/util';

const getFormData = data => {
    let formData = new FormData();

    if (data.id) {
        formData.append('id', data.id);
    }
    formData.append('title', data.title);
    formData.append('startTime', data.startTime);
    formData.append('endTime', data.endTime);
    formData.append('applyStartTime', data.signStartTime);
    formData.append('applyEndTime', data.signEndTime);
    formData.append('address', data.place);
    formData.append('intro', data.description);
    formData.append('pics', data.images);
    formData.append('cover', data.cover);

    return formData;
};
</script>