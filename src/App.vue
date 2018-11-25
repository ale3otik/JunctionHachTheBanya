<template>
    <div id="app">
        <div v-for="alert in alerts">
            <base-alert type="danger" dismissible>
                <span data-notify="message"><b>Alert:</b> {{ alert }}</span>
            </base-alert>
        </div>
        <div class="title">Sauna dashboard</div>
        <div class="charts">
            <Chart name="Stone temperature" url="temperatureBench"></Chart>
            <Chart name="CO2" url="carbonDioxide"></Chart>
            <Chart name="Ceil temperature" url="temperatureCeil"></Chart>
            <Chart name="Add firewood" url="drova" radius="2"></Chart>
        </div>
    </div>
</template>

<script>
    import Chart from './components/Chart.vue'
    import BaseAlert from './components/BaseAlert.vue';

    export default {
        name: 'app',
        components: {
            Chart: Chart,
            BaseAlert: BaseAlert
        },
        data: function() {
            return {
                alerts: []
            }
        },
        methods: {
            showAlert(message) {
                this.alerts.push(message);
            }
        }
    }
</script>

<style>
    body {
        background-color: #1E1E2F;
    }

    #app {
        font-family: 'Segoe UI Light', Helvetica, Arial, sans-serif;
        font-weight: 400;
        font-size: 1rem;
    }

    .charts {
        display: grid;
        grid-template-columns: repeat(2, 50%);
        grid-template-rows: repeat(2, auto);
    }

    .alert {
        display: inline-block;
        margin: 1rem 1rem 0.1rem;
        position: relative;
        padding: 0.9rem 1.25rem;
        border: 0.0625rem solid transparent;
        border-radius: 0.4rem;
        font-size: 1.1rem;
    }

    .alert-danger {
        color: white;
        background-color: #EF5350;
        border-color: #E53935;
    }

    .close {
        background: transparent;
        margin-left: 1em;
        border: 0;
        cursor: pointer;
        float: right;
    }

    .title {
        font-size: 3rem;
        color: #eeebeb;
        margin: 1rem;
    }
</style>
