odoo.define('calendar_event_drag_drop_conflict_check', function (require) {
    "use strict";

    var CalendarController = require('calendar.CalendarController');

    CalendarController.include({
        _onDragAndDrop: function (event) {
            // Call the original method first
            this._super.apply(this, arguments);

            // Get the event data
            var eventData = event.data.data;

            // Check for conflicts
            var self = this;
            this._rpc({
                model: 'calendar.event',
                method: 'check_event_conflict',
                args: [eventData.id, eventData.start, eventData.stop, eventData.rental_property_id],
            }).then(function (result) {
                if (result.conflict) {
                    // If there is a conflict, show an error message and revert the event
                    self.do_warn('Conflict', 'You cannot have overlapping events for the same rental property.');
                    event.revert();
                }
            });
        },
    });
});