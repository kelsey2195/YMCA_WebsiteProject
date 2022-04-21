// Automatically sets swim level to less than program name
function updateSwimLevel( progNameInput, minSwimLevelInput, swimlevels ) {
    var programLevel = swimlevels.indexOf(progNameInput.value.toLowerCase());
    if( programLevel > -1 ) {
        minSwimLevelInput.value = swimlevels[ programLevel - 1 ];
    }
}

// Makes sure that when changing start date it maintains end is after start
//TODO add a way to update error message
function whenChangeStartDate( start, end ) {
    var startDate = start.value;
    var currDate = new Date().toJSON().split("T")[0];

    // Checks if start date is before curr date
    if( startDate < currDate ){
        startDate = currDate;
        start.value = currDate;
    }

    // Checks if there is end value then check if end is before start
    if( end && end.value ) {
        if( end.value < startDate ) {
            end.value = startDate;
            //TODO update error value here "start date should be before end date"
        }
    }
}

// Makes sure that when changing end date is maintains end is after start
//TODO add a way to update error message
function whenChangeEndDate( start, end ) {
    var endDate = end.value;
    var currDate = new Date().toJSON().split("T")[0];
    
    // checks to make sure that end date is after currdate
    if( endDate < currDate ){
        endDate = currDate;
        end.value = currDate;
    }

    // Checks if there is a start value then check if end is less than start date
    if( start && start.value ) {
        if( start.value > endDate ) {
            start.value = endDate;
            //TODO update error value here "end date should be after start date"
        }
    }
}

// Makes sure that start time is before end time
//TODO add a way to update error message
function whenChangeStartTime( start, end ) {
    var startTime = start.value;

    if( end && end.value ) {
        if( end.value < startTime ) {
            end.value = startTime;
            //TODO update error value here "start date should be before end date"
        }
    }
}

// Makes sure that end time is after start time
//TODO add a way to update error message
function whenChangeEndTime( start, end ) {
    var endTime = end.value;

    if( start && start.value ) {
        if( start.value > endTime ) {
            start.value = endTime;
            //TODO update error value here "end date should be after start date"
        }
    }
}

// Makes sure that max participates never goes bellow 1
// TODO add a way to update error message
function minPeople( input ) {
    if( input.value < 1 ){
        input.value = 1;
    }
}

// Makes sure that memberprice doesn't go bellow 1 and sets nonmember to double memmber
// TODO add a way to update error message
function setNonMemberPrice( member, nonMember ) {
    if( member.value < 1 ){
        member.value = 1;
    }
    nonMember.value = member.value * 2;
}

// Makes sure that the nonMemberprice never goes bellow 1
// also checks to make sure member value is greater than nonmember price
// TODO add a way to update error message
function minNonMemberPrice( member,  nonMember ) {
    if( nonMember.value < 1 ){
        nonMember.value = 1;
    }

    var mem = member.value;
    var non = nonMember.value;

    if( mem > non ) {
        member.value = non;
    }
}

// Makes the time input nicer
function setTime( input ) {
    if( !input.value ) {
        input.value = "08:00"
    }
}