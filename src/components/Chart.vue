<template>
    <div class="main">
        <header class="header">
            {{ name }}
        </header>
        <div v-if="isLoading" class="loading">
            Loading...
        </div>
        <line-chart v-else class="chart"
                    :chart-data="chartData"
                    :extra-options="extraOptions"
                    :gradient-colors="gradientColors"></line-chart>
    </div>
</template>

<script>
    import LineChart from "./LineChart";
    import * as chartConfigs from './config';

    export default {
        name: 'Chart',
        components: {LineChart},
        props: {
            name: String,
            url: String,
            radius: {
                type: Number,
                default: 6
            }
        },
        data() {
            return {
                chartData: {
                    labels: undefined,
                    datasets: [{
                        label: "Anomaly",
                        fill: false,
                        showLine: false,
                        pointBackgroundColor: "rgb(211,47,47, 0.4)",
                        pointBorderColor: 'rgba(255,255,255,0)',
                        pointHoverBackgroundColor: "rgb(211,47,47, 0.8)",
                        pointBorderWidth: 20,
                        pointHoverRadius: undefined,
                        pointHoverBorderWidth: 15,
                        pointRadius: undefined,
                        data: undefined,
                    }, {
                        label: this.name,
                        fill: true,
                        borderColor: "#42b883",
                        borderWidth: 2,
                        pointBackgroundColor: "#42b883",
                        pointBorderColor: 'rgba(255,255,255,0)',
                        pointHoverBackgroundColor: "#42b883",
                        pointRadius: 0,
                        data: undefined,
                    }],
                },
                extraOptions: chartConfigs.purpleChartOptions,
                gradientColors: ['rgba(66,134,121,0.15)', 'rgba(66,134,121,0.0)', 'rgba(66,134,121,0)',
                    'rgb(101,153,153, 1.0)', 'rgba(66,134,121,1.0)', 'rgba(66,134,121,1.0)']
            }
        },
        mounted() {
            this.getGraph();
        },
        computed: {
            isLoading: function() {
                return this.chartData.datasets[0].data === undefined ||
                this.chartData.labels === undefined;
            }
        },
        methods: {
            sleep: function(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            },
            getGraph: function() {
                let this_ = this;
                $.ajax({
                    url: 'http://10.100.18.228:5000/' + this_.url,
                    type: 'GET',
                    dataType: 'json',
                    success: function (response) {
                        this_.chartData.labels = response.results_x.map(x => {
                            let date = new Date(x);
                            let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                                'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                            let month = months[date.getMonth()];
                            let day = date.getDate();
                            let hours = date.getHours();
                            let minutes = "0" + date.getMinutes();
                            let seconds = "0" + date.getSeconds();
                            return month + ' ' + day + ', ' +
                                hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
                        });
                        this_.chartData.datasets[1].data = response.results_y;

                        let radiuses = new Array(response.results_x.length).fill(0);
                        let anomalies = new Array(response.results_x.length).fill(0);
                        if (this_.name !== 'CO2') {
                            response.anomaly_x.push(response.results_x[response.results_x.length - 1]);
                        }
                        response.anomaly_x.forEach(x => {
                            radiuses[x] = this_.radius;
                            anomalies[x] = response.results_y[x];
                        });
                        this_.chartData.datasets[0].data = anomalies;
                        this_.chartData.datasets[0].pointRadius = radiuses;
                        this_.chartData.datasets[0].pointHoverRadius = radiuses;

                        if (response.anomaly_x[response.anomaly_x.length - 1] ===
                            response.results_x[response.results_x.length - 1]) {
                            this_.$parent.showAlert(this_.name + " is too high!");
                        }

                        // await this_.sleep(2000);
                        // this_.getGraph();
                    },
                    error: function (jqXHR, e) {
                        console.log('Error loading dataset');
                    }
                });
            }
        }
    }
</script>

<style>
    .main {
        margin: 1em;
        border-radius: 1rem;
        background-color: #27293D;
        padding: 1.5em;
    }

    .header {
        color: #c5c5c6;
        font-size: 2em;
        padding-bottom: 1em;
    }

    .loading {
        color: #c5c5c6;
    }
</style>