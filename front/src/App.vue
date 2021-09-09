<template>
  <v-app>
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title class="text-h5"> Make the decision </v-card-title>

        <v-card-text>
          Do you want to sell the stock or to continue to hold it? If you choose
          'Sell' this period will end.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="green darken-1" @click="continueKeeping">
            Continue
          </v-btn>

          <v-btn color="red darken-1" @click="sell"> Sell </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-main>
      <v-container>
        <v-row>
          <v-col>
            <v-sheet>
              <v-card elevation="4">
                <v-card-title>
                  <span>Current price:</span>
                </v-card-title>
                <v-card-text class="text-h5 font-weight-bold">
                  <h2>
                    <v-icon x-large :color="direction.color">{{
                      direction.icon
                    }}</v-icon>

                    {{ tweenedPrice }}
                  </h2>
                </v-card-text>
              </v-card>
            </v-sheet>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6"
            ><highcharts
              :constructorType="'stockChart'"
              class="hc"
              :options="chartOptions"
              ref="chart"
              :updateArgs="[true, true, true]"
            ></highcharts
          ></v-col>

          <v-col cols="6">
            <v-card elevation="4">
              <v-card-title>Instructions:</v-card-title>
              <v-card-text>
                <div>
                  If you want to sell your stock, please drag the round slider
                  below to 0.
                </div>
                <div class="d-flex align-items-center justify-center my-3">
                  <round-slider
                    rangeColor="green"
                    v-model="sliderValue"
                    start-angle="315"
                    end-angle="+270"
                    line-cap="round"
                    :valueChange="changeslider"
                  />
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
/* eslint-disable */

import RoundSlider from "vue-round-slider";
import { Chart } from "highcharts-vue";

import gsap from "gsap";
import _ from "lodash";

const formatDown = {
  color: "red",
  icon: "mdi-arrow-down-bold",
};
const formatUp = {
  color: "green darken-3",
  icon: "mdi-arrow-up-bold",
};

export default {
  name: "App",
  components: {
    highcharts: Chart,
    RoundSlider,
  },
  data: function() {
    const firstVal = window.data[0];
    return {
      sliderColor: null,
      dialog: false,
      sliderValue: 100,
      tweenedPrice: null,
      counter: 0,
      stockIntervall: null,
      tickFrequency: 1,
      chartOptions: {
        navigator: { enabled: false },
        rangeSelector: {
          inputEnabled: false,
          selected: false,
        },
        series: [
          {
            data: firstVal,
          },
        ],
      },
    };
  },
  computed: {
    direction() {
      if (this.currentPrice > this.previousPrice) {
        return formatUp;
      } else {
        return formatDown;
      }
    },
    currentPrice() {
      return _.last(window.data[this.counter]);
    },
    previousPrice() {
      const data = window.data[this.counter - 2];
      if (data) {
        return _.last(data);
      } else {
        return 0;
      }
    },
  },
  watch: {
    sliderValue(val) {
      if (val === 0) {
        this.dialog = true;
      }
    },
    currentPrice: function(newValue) {
      gsap.to(this.$data, {
        duration: 0.5,
        tweenedPrice: _.round(newValue, 3),
      });
    },
  },
  mounted() {
    this.stockInterval = setInterval(() => {
      this.counter++;
      const newData = window.data[this.counter];
      if (newData) {
        this.chartOptions.series[0].data.push(...newData);
      } else document.getElementById("form").submit();
    }, this.tickFrequency * 1000);
  },
  methods: {
    changeslider(v) {},
    continueKeeping() {
      this.sliderValue = 100;
      this.dialog = false;
    },
    sell() {
      this.dialog = false;
      document.getElementById("form").submit();
    },
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
