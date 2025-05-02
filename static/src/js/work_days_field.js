odoo.define("om_hospital.work_days", (require) => {
  const AbstractField = require("web.AbstractField");
  const core = require("web.core");
  const field_registry = require("web.field_registry");

  const QWeb = core.qweb;

  const WorkDaysWidget = AbstractField.extend({
    supportedFieldTypes: ["char"],
    className: "o_field_work_days",
    events: _.extend(
      {
        "click .o_day": "_onClickDay",
      },
      AbstractField.prototype.events
    ),

    /**
     * @override
     * @returns {boolean}
     */
    isSet: () => {
      return true;
    },

    /**
     * @private
     * @override
     */
    _render: function () {
      const info = JSON.parse(this.value) || [];
      const days = {
        sat: info.includes("sat"),
        sun: info.includes("sun"),
        mon: info.includes("mon"),
        tue: info.includes("tue"),
        wed: info.includes("wed"),
        thu: info.includes("thu"),
        fri: info.includes("fri"),
      };

      this.$el.html(QWeb.render("WorkDaysWidget", { days }));
      this.$(".o_day").each((_, el) => {
        const $el = $(el);
        const day = $el.data("day");
        if (days[day]) {
          $el.addClass("btn-primary");
          $el.removeClass("btn-secondary");
          $el.attr("data-selected", "true");
        }
        console.log("mode", this.mode);
        if (this.mode !== "edit") {
          $el.addClass("disabled");
          $el.attr("disabled", true);
        }
      });
      
    },

    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClickDay: function (ev) {
      const $target = $(ev.currentTarget);
      const selected = JSON.parse($target.attr("data-selected") || "false");

      if (selected) {
        $target.removeClass("btn-primary");
        $target.addClass("btn-secondary");
        $target.attr("data-selected", "false");
      } else {
        $target.addClass("btn-primary");
        $target.removeClass("btn-secondary");
        $target.attr("data-selected", "true");
      }

      const info = [];
      this.$(".o_day").each((_, el) => {
        const $el = $(el);
        if (JSON.parse($el.attr("data-selected") || "false") === true) {
          info.push($el.data("day"));
        }
      });
      this.value = JSON.stringify(info);
      this._setValue(this.value);
      this.trigger_up("field_changed", {
        dataPointID: this.dataPointID,
        changes: { [this.name]: this.value },
      });
    },
  });

  field_registry.add("work_days", WorkDaysWidget);

  return {
    WorkDaysWidget: WorkDaysWidget,
  };
});
