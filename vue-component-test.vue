<style type="text/css">
    .container {
    .question {
        background-color:white;
        &:after {
            content: '';
            height: rem(30);
            background-color:#f5f5f5;
            display: block;
        }
        .option {
            min-height: rem(100);
            display: flex;
            align-items:center;
            border-top: 1px solid #e5e5e5;
            justify-content: space-between;
            padding-left:rem(30);
            padding-right:rem(30);
            font-size:rem(32);
            p {
                display: flex;
                width: 100%;
                justify-content: space-between;
                padding-top:rem(34);
                padding-bottom:rem(34);
            }
            .vote {
                min-width: rem(100);
                text-align: right;
                display: block;
                font-size: rem(32);
            }
        }
        .fillin {
            font-size:rem(24);
            color: #d2ad15;
            height: rem(90);
            text-align: center;
            line-height: rem(90);
            border-top:1px solid #e5e5e5;
        }
    }
}
.question-content {
    padding-left:rem(30);
    display: flex;
    align-items:center;
    min-height: rem(100);
    font-size: rem(32);
    padding-top:rem(34);
    padding-bottom:rem(34);
}
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
    }
    ul {
        width: 100%;
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
    .answer {
        font-size: 18px;
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

const setStore = (store, data) => {
    let formData = {};

    formData.id = data.id;
    formData.title = data.title;
    formData.startTime = data.startTime;
    formData.endTime = data.endTime;
    formData.signStartTime = data.applyStartTime;
    formData.signEndTime = data.applyEndTime;
    formData.place = data.address;
    formData.description = data.intro;
    formData.images = string2Array(data.pics);
    formData.cover = data.cover;

    store.formData.set(formData);
};

export {
    getFormData,
    setStore
};
</script>