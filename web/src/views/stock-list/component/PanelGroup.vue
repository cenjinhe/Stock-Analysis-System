<template>
  <div>
    <el-row :gutter="40" class="panel-group">
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('high')">
          <div class="card-panel-icon-wrapper icon-high">
            <svg-icon name="icon-money" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              最高
            </div>
            <count-to
              :start-val="0"
              :end-val="panelNum.high"
              :decimals="2"
              :duration="1000"
              class="card-panel-num"
            />
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('low')">
          <div class="card-panel-icon-wrapper icon-low">
            <svg-icon name="icon-money" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              最低
            </div>
            <count-to
              :start-val="0"
              :end-val="panelNum.low"
              :decimals="2"
              :duration="1000"
              class="card-panel-num"
            />
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('preclose')">
          <div class="card-panel-icon-wrapper icon-preclose">
            <svg-icon name="icon-money" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              昨日收盘
            </div>
            <count-to
              :start-val="0"
              :end-val="panelNum.preclose"
              :decimals="2"
              :duration="1000"
              class="card-panel-num"
            />
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
        <div class="card-panel" @click="handleSetLineChartData('close')">
          <div class="card-panel-icon-wrapper icon-close">
            <svg-icon name="icon-money" class-name="card-panel-icon" />
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              <span>今日收盘</span>
            </div>
            <count-to
              :start-val="0"
              :end-val="panelNum.close"
              :decimals="2"
              :duration="1000"
              class="card-panel-num"
            />
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
//  https://blog.csdn.net/fengxiaopeng74/article/details/120484307
import CountTo from '@/components/vue-count-to/vue-countTo.vue'
import { getRawDataList } from '@/api/stock-manage'

export default {
  components: {
    CountTo,
  },
  props: {
    code: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      panelNum: {
        high: 0,
        low: 0,
        close: 0,
        preclose: 0,
      },
    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    initData() {
      // 数据意义：0日期(date)，1开盘(open)，2收盘(close)，3最低(low)，4最高(high)，5成交量(volume)，6昨日收盘(pre_close)
      getRawDataList({ count: 1, code: this.$props.code }).then(rep =>{
        const rawData = rep.rawData
        if (rawData && rawData.length > 0) {
          this.panelNum = {
            high: rawData[0][4],
            low: rawData[0][3],
            close: rawData[0][2],
            preclose: rawData[0][6]
          }
        }
      })
    },
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    },
  },
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 0;
  }

  .card-panel {
    height: 85px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
    border-color: rgba(0, 0, 0, 0.05);

    & {
      /*&:hover {*/
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-high {
        background: #40c9c6;
      }

      .icon-low {
        background: #36a3f7;
      }

      .icon-close {
        background: #f4516c;
      }

      .icon-preclose {
        background: #4ccb5b;
      }
    }

    .icon-high {
      color: #fff;
    }

    .icon-low {
      color: #fff;
    }

    .icon-close {
      color: #fff;
    }

    .icon-preclose {
      color: #fff;
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px 26px 26px 0;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width: 550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
