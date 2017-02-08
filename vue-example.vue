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